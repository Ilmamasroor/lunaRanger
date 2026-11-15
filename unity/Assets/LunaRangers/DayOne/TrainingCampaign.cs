using System;

namespace LunaRangers.DayOne
{
    internal enum Station { Power, Dock, Valve, Water, Scrubber, Monitor, Shelter, Suit, Airlock, Sample, Locker, Report }
    internal enum CampaignAction { Work, Exit, Collect, Return, Store }

    internal sealed class TrainingCampaign
    {
        internal const int LastDay = 7;
        internal const float DigSuitSeconds = 25f;
        internal sealed class Task
        {
            internal readonly Station Station;
            internal readonly string Label, Result;
            internal readonly CampaignAction Action;
            internal readonly PuzzleKind Puzzle;

            internal Task(Station station, string label, string result, CampaignAction action = CampaignAction.Work,
                PuzzleKind puzzle = PuzzleKind.None)
            {
                Station = station;
                Label = label;
                Result = result;
                Action = action;
                Puzzle = puzzle;
            }
        }

        internal sealed class Day
        {
            internal readonly string Title, Briefing, Debrief;
            internal readonly Task[] Tasks;

            internal Day(string title, string briefing, string debrief, Task[] tasks)
            {
                Title = title;
                Briefing = briefing;
                Debrief = debrief;
                Tasks = tasks;
            }
        }

        private static readonly Day[] Days =
        {
            new("Balance the power", "Find the power console in the west workshop.",
                "The battery stores energy for when the outpost has less sunlight.", new Task[]
                {
                    new(Station.Power, "Route backup power", "The heater, scrubber, and battery have power.", puzzle: PuzzleKind.Power)
                }),
            new("Restore water", "Find the recycler in the east lab. It cleans used water for the crew.",
                "Rerouting water through the filter restored the crew's reserve.", new Task[]
                {
                    new(Station.Valve, "Repair the water line", "Water reaches the filter. Start the recycler.", puzzle: PuzzleKind.Water),
                    new(Station.Water, "Start the recycler", "Clean water is flowing again.")
                }),
            new("Make the air safe", "The east lab's scrubber removes carbon dioxide from the air.",
                "The new filter is working, and the air monitor confirms safe cabin air.", new Task[]
                {
                    new(Station.Scrubber, "Fit a replacement filter", "The filter seals the slot. Cabin air is safe.", puzzle: PuzzleKind.Air)
                }),
            new("Shield the crew", "A solar alert has locked the airlock. Go to the west workshop shelter.",
                "Covering the exposed openings gave the crew a safer place to wait out the alert.", new Task[]
                {
                    new(Station.Shelter, "Set up the shelter", "The exposed openings are shielded.", puzzle: PuzzleKind.Shelter)
                }),
            new("Excavate a Moon rock", "Check your suit in the workshop, then take your scanner outside.",
                "You collected a Moon rock and returned safely through the airlock.", new Task[]
                {
                    new(Station.Suit, "Check your suit", "Suit ready. The timer starts when you step outside."),
                    new(Station.Airlock, "Start the moonwalk", "Follow the marker to the sample.", CampaignAction.Exit),
                    new(Station.Sample, "Scan and excavate", "Sample collected. Return to the airlock.", CampaignAction.Collect, PuzzleKind.Dig),
                    new(Station.Airlock, "Return with the sample", "You and the Moon rock are safely inside.", CampaignAction.Return)
                }),
            new("Catalog the samples", "Take the recovered rock to the east lab and sort it with the reference samples.",
                "The sample is stored, and the crew and habitat checks are complete.", new Task[]
                {
                    new(Station.Locker, "Sort and store samples", "Samples labeled and secured.", CampaignAction.Store, PuzzleKind.Sort),
                    new(Station.Report, "File the mission report", "Mission complete. The crew and sample are safe.")
                })
        };

        internal int Number { get; private set; } = 2;
        internal int Step { get; private set; }
        internal int Water { get; private set; }
        internal int Health { get; private set; }
        internal float SuitLeft { get; private set; } = DigSuitSeconds;
        internal bool Outside { get; private set; }
        internal bool CarryingSample { get; private set; }
        internal bool SampleStored { get; private set; }
        internal Day Current => Days[Number - 2];
        internal bool Complete => Step == Current.Tasks.Length;
        internal bool NeedsRetry => Health == 0;
        internal Task Next => Complete || NeedsRetry ? null : Current.Tasks[Step];

        private int startingWater, startingHealth;

        internal TrainingCampaign(int water, int health)
        {
            startingWater = Water = water;
            startingHealth = Health = health;
        }

        internal void Advance()
        {
            if (!Complete || Number == LastDay) return;
            Number++;
            startingWater = Water;
            startingHealth = Health;
            Restart();
        }

        internal void Restart()
        {
            Step = 0;
            Water = Number == 3 ? Math.Min(startingWater, 45) : startingWater;
            Health = startingHealth;
            SuitLeft = DigSuitSeconds;
            Outside = false;
            CarryingSample = Number == 7;
            SampleStored = false;
        }

        internal bool Tick(float elapsed)
        {
            if (!Outside) return false;

            SuitLeft = Math.Max(0f, SuitLeft - elapsed);
            if (SuitLeft > 0f) return false;
            Outside = false;
            CarryingSample = false;
            Health = Math.Max(0, Health - 20);
            SuitLeft = DigSuitSeconds;
            Step = 0;
            return true;
        }

        internal bool TryInteract(Station station, MissionPuzzle puzzle = null)
        {
            var task = Next;
            if (task == null || task.Station != station ||
                (task.Puzzle != PuzzleKind.None && (puzzle?.Kind != task.Puzzle || !puzzle.Solved))) return false;

            switch (task.Action)
            {
                case CampaignAction.Exit: Outside = true; break;
                case CampaignAction.Collect: CarryingSample = true; break;
                case CampaignAction.Return:
                    Outside = false;
                    SuitLeft = DigSuitSeconds;
                    break;
                case CampaignAction.Store:
                    CarryingSample = false;
                    SampleStored = true;
                    break;
            }

            if (Number == 3 && station == Station.Water) Water = 100;
            Step++;
            return true;
        }
    }
}
