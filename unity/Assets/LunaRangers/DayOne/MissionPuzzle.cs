namespace LunaRangers.DayOne
{
    internal enum PuzzleKind { None, Power, Water, Air, Shelter, Dig, Sort }

    internal sealed class MissionPuzzle
    {
        internal const int North = 1, East = 2, South = 4, West = 8;
        private static readonly string[] Loads = { "Heater   3", "Air scrubber   3", "Battery charger   2", "Cabin lights   2", "Lab tools   2" };
        private static readonly int[] Costs = { 3, 3, 2, 2, 2 };
        private static readonly string[] Filters = { "Round / 1 bar", "Square / 2 bar", "Round / 2 bar" };
        private static readonly string[] Shields = { "Hatch   2 kg", "Window   3 kg", "Roof   4 kg", "Floor   2 kg" };
        private static readonly int[] Weights = { 2, 3, 4, 2 };
        private static readonly string[] Samples = {
            "Pale and grainy, with visible crystals.",
            "Loose gray powder with no solid pieces.",
            "Dark, solid, and full of tiny holes."
        };
        private static readonly int[] SampleBins = { 1, 2, 0 };
        private readonly int[] pipes = { 3, 5, 9, 12, 10, 9, 6, 3, 5 };
        private int selected, progress, digTool;
        private bool scanned;

        internal MissionPuzzle(PuzzleKind kind) { Kind = kind; }
        internal PuzzleKind Kind { get; }
        internal bool Solved { get; private set; }
        internal string Feedback { get; private set; } = "";
        internal string Title => Kind switch
        {
            PuzzleKind.Power => "Balance the power",
            PuzzleKind.Water => "Rebuild the water line",
            PuzzleKind.Air => "Fit a new air filter",
            PuzzleKind.Shelter => "Shield the crew",
            PuzzleKind.Dig => "Excavate the signal",
            _ => "Sort the samples"
        };
        internal string Instructions => Kind switch
        {
            PuzzleKind.Power => "Switch on the heater, air scrubber, and battery charger. You have 8 power units.",
            PuzzleKind.Water => "Click a pipe to turn it. Route water from the left inlet through the filter to the right outlet.",
            PuzzleKind.Air => "Read the slot label, then install the filter with the matching shape and pressure.",
            PuzzleKind.Shelter => "Cover the exposed hatch and window. The crew can carry up to 6 kg.",
            PuzzleKind.Dig => "Scan for a buried rock. Brush the strong signal twice, then lift the sample.",
            _ => "Match each specimen to the bin that describes it."
        };
        internal string Reading => Kind switch
        {
            PuzzleKind.Power => $"{Total(Costs)} / 8 power units in use",
            PuzzleKind.Water => "Left inlet   >   Top filter   >   Right outlet",
            PuzzleKind.Air => "SLOT LABEL   Round connector / 2 bar",
            PuzzleKind.Shelter => $"{Total(Weights)} / 6 kg   |   Hatch and window exposed",
            PuzzleKind.Dig => !scanned ? "Scanner off" : progress == 2 ? "Rock exposed. Lift it carefully." : "Strong signal near the center.",
            _ => Solved ? "All three samples labeled" : $"SPECIMEN {progress + 1} / 3   {Samples[progress]}"
        };
        internal string Hint => Kind switch
        {
            PuzzleKind.Power => "Keep heat and clean air running. Turn off the lights and lab to free power for charging.",
            PuzzleKind.Water => "Try the top row. Both ends of each pipe must touch the next pipe.",
            PuzzleKind.Air => "Two filters are round. Check the pressure rating too.",
            PuzzleKind.Shelter => "The hatch and window weigh 5 kg together. Leave the other panels behind.",
            PuzzleKind.Dig => "The strongest scanner reading is B2. Use Brush there twice, then Lift.",
            _ => "Check whether the specimen is loose dust, pale crystals, or dark rock with holes."
        };

        internal int Count => Kind switch
        {
            PuzzleKind.Power => 6, PuzzleKind.Water => 10, PuzzleKind.Shelter => 5,
            PuzzleKind.Dig => 12, _ => 3
        };
        internal bool IsGrid => Kind == PuzzleKind.Water || Kind == PuzzleKind.Dig;
        internal int Pipe(int slot) => Kind == PuzzleKind.Water && slot < pipes.Length ? pipes[slot] : 0;
        internal bool IsActive(int slot) => Kind switch
        {
            PuzzleKind.Power => slot < Loads.Length && (selected & (1 << slot)) != 0,
            PuzzleKind.Shelter => slot < Shields.Length && (selected & (1 << slot)) != 0,
            PuzzleKind.Water => slot == 1 || slot == 3 || slot == 5,
            PuzzleKind.Dig => (scanned && slot == 4) || (slot == 10 && digTool == 1) || (slot == 11 && digTool == 2),
            _ => false
        };

        internal string Label(int slot) => Kind switch
        {
            PuzzleKind.Power => slot == 5 ? "Send power" : Loads[slot],
            PuzzleKind.Water => slot == 9 ? "Test water flow" : slot switch { 1 => "Filter", 3 => "Inlet", 5 => "Outlet", _ => "" },
            PuzzleKind.Air => Filters[slot],
            PuzzleKind.Shelter => slot == 4 ? "Check shelter" : Shields[slot],
            PuzzleKind.Dig => slot switch
            {
                9 => "Scan", 10 => "Brush", 11 => "Lift",
                4 when progress == 2 => "Exposed rock",
                4 when scanned => "B2   Strong signal",
                _ => $"{(char)('A' + slot / 3)}{slot % 3 + 1}" + (scanned ? "   Weak signal" : "")
            },
            _ => slot switch { 0 => "Dark porous rock", 1 => "Pale crystal rock", _ => "Loose lunar dust" }
        };

        internal void Press(int slot)
        {
            if (Solved || slot < 0 || slot >= Count) return;
            Feedback = "";
            switch (Kind)
            {
                case PuzzleKind.Power:
                    if (slot < Loads.Length) selected ^= 1 << slot;
                    else if (selected == 7) Solved = true;
                    else Feedback = Total(Costs) > 8 ? "Too much demand. Switch something off." : "Keep heat, clean air, and charging online.";
                    break;
                case PuzzleKind.Water:
                    if (slot < pipes.Length) pipes[slot] = ((pipes[slot] << 1) & 15) | (pipes[slot] >> 3);
                    else if (WaterFlows()) Solved = true;
                    else Feedback = "The water stopped. Look for an open pipe end.";
                    break;
                case PuzzleKind.Air:
                    if (slot == 2) Solved = true;
                    else Feedback = slot == 0 ? "The shape fits, but this filter is rated too low." : "A square filter won't seal the round slot.";
                    break;
                case PuzzleKind.Shelter:
                    if (slot < Shields.Length) selected ^= 1 << slot;
                    else if ((selected & 3) == 3 && Total(Weights) <= 6) Solved = true;
                    else Feedback = Total(Weights) > 6 ? "The crew can't carry that much. Remove a panel." : "Both the hatch and window need covering.";
                    break;
                case PuzzleKind.Dig:
                    if (slot == 9) { scanned = true; digTool = 0; }
                    else if (slot >= 10) digTool = slot - 9;
                    else if (!scanned || digTool == 0) Feedback = "Scan the ground, then select a tool.";
                    else if (slot != 4) Feedback = "Nothing here. Check the strongest signal.";
                    else if (digTool == 1 && progress < 2) { progress++; Feedback = progress == 1 ? "One more brush will uncover the rock." : ""; }
                    else if (digTool == 2 && progress == 2) Solved = true;
                    else Feedback = progress == 2 ? "Switch to Lift to collect the rock." : "Brush away the dust before lifting.";
                    break;
                case PuzzleKind.Sort:
                    if (slot == SampleBins[progress])
                    {
                        progress++;
                        Solved = progress == Samples.Length;
                        Feedback = "Sample labeled. Inspect the next one.";
                    }
                    else Feedback = "Look at the specimen again and match its description.";
                    break;
            }
        }

        private int Total(int[] values)
        {
            int total = 0;
            for (int i = 0; i < values.Length; i++)
                if ((selected & (1 << i)) != 0) total += values[i];
            return total;
        }

        private bool WaterFlows()
        {
            int tile = 3, entry = West, seen = 0;
            while ((seen & (1 << tile)) == 0 && (pipes[tile] & entry) != 0)
            {
                seen |= 1 << tile;
                int exit = pipes[tile] ^ entry;
                if (tile == 5 && exit == East) return (seen & (1 << 1)) != 0;
                int next = exit switch
                {
                    North when tile >= 3 => tile - 3,
                    East when tile % 3 != 2 => tile + 1,
                    South when tile < 6 => tile + 3,
                    West when tile % 3 != 0 => tile - 1,
                    _ => -1
                };
                if (next < 0) break;
                tile = next;
                entry = exit < South ? exit << 2 : exit >> 2;
            }
            return false;
        }
    }
}
