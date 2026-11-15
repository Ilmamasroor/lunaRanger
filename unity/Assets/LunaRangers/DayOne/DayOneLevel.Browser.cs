using System;
using System.Runtime.InteropServices;
using UnityEngine;

namespace LunaRangers.DayOne
{
    public sealed partial class DayOneLevel
    {
        [Serializable]
        private sealed class BrowserState
        {
            public int day, step, secondsLeft, suitOxygen, water, health;
            public bool outside, finished, needsRetry;
            public string feedback;
        }

        [Serializable]
        private sealed class ClearanceResult
        {
            public int token;
            public bool approved;
            public string requestId, reason, message;
        }

        private readonly BrowserState browserState = new();
        private bool engineClearance;
        private int clearanceSequence, pendingClearance;
        private float clearanceDeadline;
        internal bool HasCampaignHost { get; private set; }

#if UNITY_WEBGL && !UNITY_EDITOR
        [DllImport("__Internal")] private static extern void PublishCampaignState(string json);
        [DllImport("__Internal")] private static extern void RequestCampaignSpacewalk(int token, int day);
#endif

        public void SetCampaignHost(string mode)
        {
            if (mode != "training" && mode != "engine") return;
            HasCampaignHost = true;
            engineClearance = mode == "engine";
            pendingClearance = 0;
            browserState.day = 0;
#if UNITY_WEBGL && !UNITY_EDITOR
            WebGLInput.captureAllKeyboardInput = false;
#endif
        }

        public void ResumeCampaignDay(string day)
        {
            if (HasCampaignHost && int.TryParse(day, out int requested) && requested == DayNumber + 1)
                RequestNextDay();
        }

        private bool AwaitSpacewalkClearance()
        {
            if (!engineClearance) return false;
            if (pendingClearance != 0) return true;
            pendingClearance = ++clearanceSequence;
            clearanceDeadline = Time.unscaledTime + 8f;
            Feedback = "Checking spacewalk clearance.";
#if UNITY_WEBGL && !UNITY_EDITOR
            RequestCampaignSpacewalk(pendingClearance, DayNumber);
#endif
            return true;
        }

        public void ApplySpacewalkDecision(string json)
        {
            if (pendingClearance == 0 || string.IsNullOrWhiteSpace(json)) return;
            ClearanceResult decision;
            try { decision = JsonUtility.FromJson<ClearanceResult>(json); }
            catch (ArgumentException) { return; }
            if (decision == null || decision.token != pendingClearance) return;
            pendingClearance = 0;
            if (!decision.approved || string.IsNullOrEmpty(decision.requestId))
            {
                Report(string.IsNullOrWhiteSpace(decision.message) ? "Spacewalk clearance unavailable. Try again." : decision.message, warningTone);
                return;
            }
            if (Outside || !Near(insideAirlock)) return;
            if (Campaign?.Next?.Action == CampaignAction.Exit) CompleteCampaignTask(Campaign.Next);
            else if (Campaign == null && Mission.Step == MissionStep.Exit)
            {
                StartBatterySpacewalk();
                ApplyMissionState();
            }
        }

        private void UpdateCampaignHost()
        {
            if (pendingClearance != 0 && Time.unscaledTime >= clearanceDeadline)
            {
                pendingClearance = 0;
                Report("Clearance timed out. Try again.", warningTone);
            }
#if UNITY_WEBGL && !UNITY_EDITOR
            if (!HasCampaignHost) return;
            int step = Campaign?.Step ?? (int)Mission.Step;
            int secondsLeft = Outside ? Mathf.CeilToInt(SecondsLeft) : 0;
            if (browserState.day == DayNumber && browserState.step == step && browserState.secondsLeft == secondsLeft &&
                browserState.water == Water && browserState.health == Health && browserState.feedback == Feedback &&
                browserState.outside == Outside && browserState.finished == Finished && browserState.needsRetry == NeedsRetry) return;
            browserState.day = DayNumber;
            browserState.step = step;
            browserState.secondsLeft = secondsLeft;
            browserState.suitOxygen = Mathf.CeilToInt(SecondsLeft / SuitLimit * 100f);
            browserState.water = Water;
            browserState.health = Health;
            browserState.outside = Outside;
            browserState.finished = Finished;
            browserState.needsRetry = NeedsRetry;
            browserState.feedback = Feedback;
            PublishCampaignState(JsonUtility.ToJson(browserState));
#endif
        }
    }
}
