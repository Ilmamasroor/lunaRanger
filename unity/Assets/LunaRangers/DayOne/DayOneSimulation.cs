using System;

namespace LunaRangers.DayOne
{
    public enum MissionStep { Exit, Collect, Return, Dock, Repair, Complete, Retry }

    public sealed class DayOneSimulation
    {
        public const float SuitLimitSeconds = 10f;
        private const int RecoveryCost = 10;
        private const int ExposurePenalty = 20;

        public MissionStep Step { get; private set; } = MissionStep.Exit;
        public float SecondsLeft { get; private set; } = SuitLimitSeconds;
        public int Water { get; private set; } = 100;
        public int Health { get; private set; } = 100;
        public int ConnectedWires { get; private set; }
        public bool Outside => Step == MissionStep.Collect || Step == MissionStep.Return;
        public int SuitOxygen => (int)Math.Ceiling(SecondsLeft / SuitLimitSeconds * 100f);
        public bool PowerRestored => Step == MissionStep.Repair || Step == MissionStep.Complete;
        public bool HeaterOn => Step == MissionStep.Complete;

        public bool TryAdvance(MissionStep action)
        {
            if (Step != action || action < MissionStep.Exit || action > MissionStep.Dock)
                return false;

            Step++;
            if (action == MissionStep.Return)
                SecondsLeft = SuitLimitSeconds;
            return true;
        }

        public bool Tick(float elapsed)
        {
            if (!Outside || elapsed <= 0f)
                return false;

            SecondsLeft = Math.Max(0f, SecondsLeft - elapsed);
            if (SecondsLeft > 0f)
                return false;

            Health = Math.Max(0, Health - ExposurePenalty);
            Step = Health > 0 ? MissionStep.Exit : MissionStep.Retry;
            if (Health > 0)
                SecondsLeft = SuitLimitSeconds;
            return true;
        }

        public bool TryDrinkWater()
        {
            if (Outside || Step >= MissionStep.Complete || Health >= 100 || Water < RecoveryCost)
                return false;

            Water -= RecoveryCost;
            Health = Math.Min(100, Health + ExposurePenalty);
            return true;
        }

        public bool TryConnect(int plug, int socket)
        {
            if (Step != MissionStep.Repair || plug < 0 || plug > 1 || plug != socket)
                return false;

            int wire = 1 << plug;
            if ((ConnectedWires & wire) != 0)
                return false;

            ConnectedWires |= wire;
            if (ConnectedWires == 3)
                Step = MissionStep.Complete;
            return true;
        }
    }
}
