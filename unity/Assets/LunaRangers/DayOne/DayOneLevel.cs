using UnityEngine;
using UnityEngine.InputSystem;

namespace LunaRangers.DayOne
{
    public sealed class DayOneLevel : MonoBehaviour
    {
        public Camera sceneCamera;
        public CharacterController player;
        public GameObject outsideBattery, carriedBattery, dockedBattery, heaterLight;
        public Transform insideStart, outsideStart, insideView, outsideView;
        public Transform insideAirlock, outsideAirlock, batteryPickup, dock, heater, waterStation;
        public DayOneHud hud;

        public DayOneSimulation Mission { get; private set; }
        public string Feedback { get; private set; }
        public int SelectedPlug { get; private set; } = -1;
        public bool WiringOpen { get; private set; }

        private AudioSource audioSource;
        private AudioClip actionTone, warningTone, finishTone;
        private InputAction interactKey, restartKey, closeKey, firstKey, secondKey;
        private int lastSecond;
        private const float WalkSpeed = 4.2f;
        private const float Reach = 1.45f;

        private void Start()
        {
            audioSource = GetComponent<AudioSource>();
            actionTone = CreateTone(600f, .12f);
            warningTone = CreateTone(330f, .16f);
            finishTone = CreateTone(880f, .45f);
            interactKey = KeyboardButton("e");
            restartKey = KeyboardButton("r");
            closeKey = KeyboardButton("escape");
            firstKey = KeyboardButton("1");
            secondKey = KeyboardButton("2");
            hud.Build(this);
            RestartDay();
        }

        private void Update()
        {
            if (Mission.Tick(Time.deltaTime))
            {
                PlacePlayer(false);
                ApplyMissionState();
                Report(Mission.Step == MissionStep.Retry
                    ? "Training paused. Restart to try again."
                    : "Time ran out. You are back inside and lost some health. Drink water or try again.", warningTone);
            }

            if (Mission.Outside)
            {
                int second = Mathf.CeilToInt(Mission.SecondsLeft);
                if (second != lastSecond && second <= 3)
                    audioSource.PlayOneShot(warningTone);
                lastSecond = second;
            }

            if (restartKey.triggered)
                RestartDay();

            if (WiringOpen)
            {
                if (closeKey.triggered) CloseWiring();
                else if (firstKey.triggered) ChooseWire(0);
                else if (secondKey.triggered) ChooseWire(1);
            }
            else if (Mission.Step < MissionStep.Complete)
            {
                var keyboard = Keyboard.current;
                if (keyboard != null)
                    Move(ReadMovement(keyboard), Time.deltaTime);
                if (interactKey.triggered)
                    Interact();
            }

            hud.Show(this, InteractionPrompt());
        }

        private static Vector2 ReadMovement(Keyboard keyboard)
        {
            int right = keyboard.dKey.isPressed || keyboard.rightArrowKey.isPressed ? 1 : 0;
            int left = keyboard.aKey.isPressed || keyboard.leftArrowKey.isPressed ? 1 : 0;
            int up = keyboard.wKey.isPressed || keyboard.upArrowKey.isPressed ? 1 : 0;
            int down = keyboard.sKey.isPressed || keyboard.downArrowKey.isPressed ? 1 : 0;
            return new Vector2(right - left, up - down);
        }

        private void Move(Vector2 input, float dt)
        {
            if (input.sqrMagnitude == 0f) return;

            Vector3 right = Vector3.ProjectOnPlane(sceneCamera.transform.right, Vector3.up).normalized;
            Vector3 forward = Vector3.Cross(right, Vector3.up);
            Vector3 direction = (right * input.x + forward * input.y).normalized;
            Vector3 position = player.transform.position;
            Vector3 next = position + direction * (WalkSpeed * dt);
            if (Mission.Outside)
            {
                next.x = Mathf.Clamp(next.x, -7.2f, -1.45f);
                next.z = Mathf.Clamp(next.z, -5.7f, -1.45f);
            }
            else
            {
                next.x = Mathf.Clamp(next.x, 75.6f, 84.4f);
                next.z = Mathf.Clamp(next.z, -4.1f, 3.7f);
            }

            player.Move(next - position);
            player.transform.rotation = Quaternion.LookRotation(direction);
        }

        private string InteractionPrompt()
        {
            if (WiringOpen || Mission.Step >= MissionStep.Complete) return "";
            if (Mission.Outside)
            {
                if (Mission.Step == MissionStep.Collect && Near(batteryPickup)) return "E  Pick up battery";
                if (Near(outsideAirlock))
                    return Mission.Step == MissionStep.Return ? "E  Return inside" : "Pick up the battery first";
                return "";
            }

            if (Mission.Health < 100 && Mission.Water >= 10 && Near(waterStation))
                return "E  Drink water to recover health";
            if (Mission.Step == MissionStep.Exit && Near(insideAirlock)) return "E  Step outside and start the timer";
            if (Mission.Step == MissionStep.Dock && Near(dock)) return "E  Plug in the battery";
            if (Mission.Step == MissionStep.Repair && Near(heater)) return "E  Inspect heater wires";
            return "";
        }

        public void Interact()
        {
            if (WiringOpen) return;
            if (Mission.Step == MissionStep.Exit && Near(insideAirlock) && Mission.TryAdvance(MissionStep.Exit))
            {
                lastSecond = (int)DayOneSimulation.SuitLimitSeconds;
                PlacePlayer(true);
                Report("Battery outside. Pick it up and return to the orange airlock.", actionTone);
            }
            else if (Mission.Step == MissionStep.Collect && Near(batteryPickup) && Mission.TryAdvance(MissionStep.Collect))
                Report("Battery collected. Return to the orange airlock.", actionTone);
            else if (Mission.Step == MissionStep.Return && Near(outsideAirlock) && Mission.TryAdvance(MissionStep.Return))
            {
                PlacePlayer(false);
                Report("Safely inside. Take the battery to the dock.", actionTone);
            }
            else if (Mission.Step == MissionStep.Dock && Near(dock) && Mission.TryAdvance(MissionStep.Dock))
                Report("Battery connected. Go to the heater and match its wires.", actionTone);
            else if (Mission.Step == MissionStep.Repair && Near(heater))
            {
                WiringOpen = true;
                Report("Choose a plug, then its matching socket.", actionTone);
            }
            else if (Near(waterStation) && Mission.TryDrinkWater())
                Report("You drank water and recovered some health.", actionTone);

            ApplyMissionState();
        }

        public void ChooseWire(int choice)
        {
            if (!WiringOpen || Mission.Step != MissionStep.Repair || choice < 0 || choice > 1)
                return;

            if (SelectedPlug < 0)
            {
                if ((Mission.ConnectedWires & (1 << choice)) != 0) return;
                SelectedPlug = choice;
                Report("Now choose the matching socket.", actionTone);
                return;
            }

            bool matched = Mission.TryConnect(SelectedPlug, choice);
            SelectedPlug = -1;
            if (Mission.HeaterOn)
            {
                CloseWiring();
                Report("Heat restored. The heater needs power from the battery.", finishTone);
            }
            else if (matched)
                Report("Connector matched. Connect the other wire.", actionTone);
            else
                Report("The shapes did not match. Choose the plug again.", warningTone);
            ApplyMissionState();
        }

        public void CloseWiring()
        {
            SelectedPlug = -1;
            WiringOpen = false;
        }

        public void RestartDay()
        {
            Mission = new DayOneSimulation();
            CloseWiring();
            PlacePlayer(false);
            ApplyMissionState();
            Feedback = "Restore heat. Start at the orange airlock.";
        }

        private bool Near(Transform target)
        {
            Vector3 distance = player.transform.position - target.position;
            distance.y = 0f;
            return distance.sqrMagnitude <= Reach * Reach;
        }

        private void PlacePlayer(bool outside)
        {
            Transform spawn = outside ? outsideStart : insideStart;
            Transform view = outside ? outsideView : insideView;
            player.enabled = false;
            player.transform.SetPositionAndRotation(spawn.position, spawn.rotation);
            player.enabled = true;
            sceneCamera.transform.SetPositionAndRotation(view.position, view.rotation);
        }

        private void ApplyMissionState()
        {
            outsideBattery.SetActive(Mission.Step <= MissionStep.Collect);
            carriedBattery.SetActive(Mission.Step == MissionStep.Return || Mission.Step == MissionStep.Dock);
            dockedBattery.SetActive(Mission.PowerRestored);
            heaterLight.SetActive(Mission.HeaterOn);
        }

        private void Report(string message, AudioClip tone)
        {
            Feedback = message;
            audioSource.PlayOneShot(tone);
        }

        private static InputAction KeyboardButton(string key)
        {
            var action = new InputAction(type: InputActionType.Button, binding: "<Keyboard>/" + key);
            action.Enable();
            return action;
        }

        private void OnDestroy()
        {
            interactKey?.Dispose();
            restartKey?.Dispose();
            closeKey?.Dispose();
            firstKey?.Dispose();
            secondKey?.Dispose();
        }

        private static AudioClip CreateTone(float frequency, float seconds)
        {
            const int rate = 22050;
            int count = Mathf.CeilToInt(rate * seconds);
            var samples = new float[count];
            for (int i = 0; i < samples.Length; i++)
            {
                float fade = Mathf.Min(i / 200f, 1f - i / (float)count);
                samples[i] = Mathf.Sin(2f * Mathf.PI * frequency * i / rate) * fade * .16f;
            }
            var clip = AudioClip.Create("Training cue", count, 1, rate, false);
            clip.SetData(samples, 0);
            return clip;
        }
    }
}
