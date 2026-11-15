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
        public Transform[] campaignStations;
        public GameObject carriedSample, storedSample, solarStatus;
        public DayOneHud hud;
        public Transform cadetBody, leftBoot, rightBoot, leftArm, rightArm;
        public bool hasAnnexes;

        public DayOneSimulation Mission { get; private set; }
        internal TrainingCampaign Campaign { get; private set; }
        internal int DayNumber => Campaign?.Number ?? 1;
        internal bool Finished => Campaign?.Complete ?? Mission.HeaterOn;
        internal bool NeedsRetry => Campaign?.NeedsRetry ?? (Mission.Step == MissionStep.Retry);
        internal bool Outside => Campaign?.Outside ?? Mission.Outside;
        internal float SuitLimit => Campaign == null ? DayOneSimulation.SuitLimitSeconds : TrainingCampaign.DigSuitSeconds;
        internal float SecondsLeft => Campaign?.SuitLeft ?? Mission.SecondsLeft;
        internal int Water => Campaign?.Water ?? Mission.Water;
        internal int Health => Campaign?.Health ?? Mission.Health;
        internal string ObjectiveName => Campaign == null ? Mission.Step switch
        {
            MissionStep.Collect => "Spare battery",
            MissionStep.Dock => "Battery dock",
            MissionStep.Repair => "Heater",
            _ => "Airlock"
        } : Campaign.Next?.Station switch
        {
            Station.Power => "Power console",
            Station.Dock => "Battery dock",
            Station.Valve => "Pipe workshop",
            Station.Water => "Water recycler",
            Station.Scrubber => "Air scrubber",
            Station.Monitor => "Cabin monitor",
            Station.Shelter => "Crew shelter",
            Station.Suit => "Suit station",
            Station.Sample => "Dig site",
            Station.Locker => "Sample locker",
            Station.Report => "Mission terminal",
            _ => "Airlock"
        };
        public string Feedback { get; private set; }
        public int SelectedPlug { get; private set; } = -1;
        public bool WiringOpen { get; private set; }
        internal MissionPuzzle Puzzle { get; private set; }
        internal bool PuzzleOpen { get; private set; }
        public Transform Objective => Campaign != null
            ? (Campaign.Next == null ? null : Locate(Campaign.Next.Station))
            : Mission.Step switch
        {
            MissionStep.Exit => insideAirlock,
            MissionStep.Collect => batteryPickup,
            MissionStep.Return => outsideAirlock,
            MissionStep.Dock => dock,
            MissionStep.Repair => heater,
            _ => null
        };

        private AudioSource audioSource;
        private AudioClip actionTone, warningTone, finishTone, connectorClick;
        private InputAction interactKey, restartKey, closeKey, firstKey, secondKey, thirdKey;
        private int lastSecond;
        private Vector3 velocity;
        private float fallSpeed, stride, gait, warmup;
        private bool advanceRequested;
        private Light heaterGlow;
        private Transform cameraView;
        private Vector3 cameraOffset;
        private const float WalkSpeed = 4.2f;
        private const float Reach = 1.45f;

        private void Start()
        {
            audioSource = GetComponent<AudioSource>();
            actionTone = CreateTone(600f, .12f);
            warningTone = CreateTone(330f, .16f);
            finishTone = CreateTone(880f, .45f);
            connectorClick = Resources.Load<AudioClip>("Heater/Click");
            interactKey = KeyboardButton("e");
            restartKey = KeyboardButton("r");
            closeKey = KeyboardButton("escape");
            firstKey = KeyboardButton("1");
            secondKey = KeyboardButton("2");
            thirdKey = KeyboardButton("3");
            heaterGlow = heaterLight.GetComponentInChildren<Light>(true);
            hud.Build(this);
            RestartDay();
        }

        private void Update()
        {
            if (advanceRequested)
            {
                advanceRequested = false;
                AdvanceDay();
            }

            if (Campaign?.Tick(Time.deltaTime) ?? Mission.Tick(Time.deltaTime))
            {
                PuzzleOpen = false;
                Puzzle = null;
                PlacePlayer(false);
                ApplyMissionState();
                Report(NeedsRetry
                    ? "Training paused. Restart to try again."
                    : Campaign == null
                        ? "You're back inside. Drink water to recover, or try again."
                        : "You're back inside. Check your suit and try again.", warningTone);
            }

            if (Outside)
            {
                int second = Mathf.CeilToInt(SecondsLeft);
                if (second != lastSecond && second <= 3)
                    audioSource.PlayOneShot(warningTone);
                lastSecond = second;
            }

            if (restartKey.triggered)
                RestartDay();

            if (WiringOpen)
            {
                velocity = Vector3.zero;
                if (closeKey.triggered) CloseWiring();
                else if (firstKey.triggered) ChooseWire(0);
                else if (secondKey.triggered) ChooseWire(1);
                else if (thirdKey.triggered) ChooseWire(2);
            }
            else if (PuzzleOpen)
            {
                if (closeKey.triggered) ClosePuzzle();
            }
            else if (!Finished && !NeedsRetry)
            {
                var keyboard = Keyboard.current;
                Move(keyboard != null ? ReadMovement(keyboard) : Vector2.zero, Time.deltaTime);
                if (interactKey.triggered)
                    Interact();
            }

            hud.Show(this, InteractionPrompt());
        }

        private void LateUpdate()
        {
            if (cameraView == null) return;
            Vector3 spawn = Outside ? outsideStart.position : insideStart.position;
            Vector3 follow = player.transform.position - spawn;
            follow.y = 0f;
            Vector3 target = Vector3.ClampMagnitude(follow * .16f, .8f);
            if (!Outside && hasAnnexes)
                target.x += Mathf.Clamp(follow.x * .85f, -10f, 10f);
            cameraOffset = Vector3.Lerp(cameraOffset, target, 1f - Mathf.Exp(-5f * Time.deltaTime));
            sceneCamera.transform.position = cameraView.position + cameraOffset;
            hud.FollowObjective(this);
            if (heaterGlow != null && Mission.HeaterOn)
            {
                warmup = Mathf.MoveTowards(warmup, 1f, Time.deltaTime * 1.8f);
                heaterGlow.intensity = warmup * 4.5f;
            }
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
            Vector3 right = Vector3.ProjectOnPlane(sceneCamera.transform.right, Vector3.up).normalized;
            Vector3 forward = Vector3.Cross(right, Vector3.up);
            Vector3 direction = (right * input.x + forward * input.y).normalized;
            velocity = Vector3.MoveTowards(velocity, direction * WalkSpeed, (input == Vector2.zero ? 42f : 30f) * dt);
            Vector3 position = player.transform.position;
            Vector3 next = position + velocity * dt;
            if (Outside)
            {
                next.x = Mathf.Clamp(next.x, -7.2f, -1.45f);
                next.z = Mathf.Clamp(next.z, -5.7f, -1.45f);
            }
            else
            {
                next.x = Mathf.Clamp(next.x, hasAnnexes ? 65.5f : 75.6f, hasAnnexes ? 94.5f : 84.4f);
                next.z = Mathf.Clamp(next.z, -4.1f, 3.7f);
            }

            if (player.isGrounded && fallSpeed < 0f) fallSpeed = -.4f;
            fallSpeed = Mathf.Max(fallSpeed - (Outside ? 1.62f : 9.81f) * dt, -12f);
            next.y += fallSpeed * dt;
            player.Move(next - position);

            Vector3 moved = player.transform.position - position;
            moved.y = 0f;
            if (direction.sqrMagnitude > .01f)
                player.transform.rotation = Quaternion.RotateTowards(player.transform.rotation, Quaternion.LookRotation(direction), 900f * dt);
            if (cadetBody != null)
            {
                float speed = moved.magnitude / Mathf.Max(.001f, dt);
                gait = Mathf.MoveTowards(gait, Mathf.Clamp01(speed / WalkSpeed), dt * 11f);
                stride += moved.magnitude * 6.8f;
                if (gait <= .01f) stride = 0f;
                PoseCadet();
            }
        }

        private void PoseCadet()
        {
            if (cadetBody == null) return;
            float step = Mathf.Sin(stride);
            cadetBody.localPosition = Vector3.up * (.105f * Mathf.Abs(step) * gait);
            cadetBody.localRotation = Quaternion.Euler(5f * gait, 0f, step * gait * 8f);
            leftBoot.localPosition = new Vector3(-.24f, .43f + Mathf.Max(0f, step) * gait * .12f, step * gait * .18f);
            rightBoot.localPosition = new Vector3(.24f, .43f + Mathf.Max(0f, -step) * gait * .12f, -step * gait * .18f);
            leftBoot.localRotation = Quaternion.Euler(step * gait * 22f, 0f, 0f);
            rightBoot.localRotation = Quaternion.Euler(-step * gait * 22f, 0f, 0f);
            leftArm.localRotation = Quaternion.Euler(-step * gait * 14f, 0f, -10f);
            rightArm.localRotation = Quaternion.Euler(step * gait * 14f, 0f, 10f);
        }

        private string InteractionPrompt()
        {
            if (Campaign != null)
            {
                if (Campaign.Next == null || PuzzleOpen) return "";
                if (DayNumber == 5 && Near(insideAirlock))
                    return "Airlock locked during solar alert";
                var target = Objective;
                return target != null && Near(target) ? "E  " + Campaign.Next.Label : "";
            }
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
            if (Mission.Step == MissionStep.Exit && Near(insideAirlock)) return "E  Step outside";
            if (Mission.Step == MissionStep.Dock && Near(dock)) return "E  Dock the battery";
            if (Mission.Step == MissionStep.Repair && Near(heater)) return "E  Open the heater panel";
            return "";
        }

        public void Interact()
        {
            if (Campaign != null)
            {
                var task = Campaign.Next;
                var target = Objective;
                if (task == null || target == null || !Near(target) || PuzzleOpen) return;
                if (task.Puzzle != PuzzleKind.None)
                {
                    Puzzle ??= new MissionPuzzle(task.Puzzle);
                    PuzzleOpen = true;
                    ResetMotion();
                    return;
                }
                CompleteCampaignTask(task);
                return;
            }
            if (WiringOpen) return;
            if (Mission.Step == MissionStep.Exit && Near(insideAirlock) && Mission.TryAdvance(MissionStep.Exit))
            {
                lastSecond = (int)DayOneSimulation.SuitLimitSeconds;
                PlacePlayer(true);
                Report("Grab the spare battery and get back before time runs out.", actionTone);
            }
            else if (Mission.Step == MissionStep.Collect && Near(batteryPickup) && Mission.TryAdvance(MissionStep.Collect))
                Report("You've got the battery. Head back to the airlock.", actionTone);
            else if (Mission.Step == MissionStep.Return && Near(outsideAirlock) && Mission.TryAdvance(MissionStep.Return))
            {
                PlacePlayer(false);
                Report("You're safe inside. Take the battery to its dock.", actionTone);
            }
            else if (Mission.Step == MissionStep.Dock && Near(dock) && Mission.TryAdvance(MissionStep.Dock))
                Report("The battery is connected. Head to the heater panel.", actionTone);
            else if (Mission.Step == MissionStep.Repair && Near(heater))
            {
                WiringOpen = true;
                ResetMotion();
                Report("Match each plug to the socket with the same shape.", actionTone);
            }
            else if (Near(waterStation) && Mission.TryDrinkWater())
                Report("You drank water and recovered some health.", actionTone);

            ApplyMissionState();
        }

        internal void PressPuzzle(int slot)
        {
            if (!PuzzleOpen || Puzzle == null) return;
            Puzzle.Press(slot);
            if (Puzzle.Solved) CompleteCampaignTask(Campaign.Next);
            else if (Puzzle.Feedback.Length > 0 && (Puzzle.Kind != PuzzleKind.Dig || slot != 4))
                audioSource.PlayOneShot(warningTone);
        }

        internal void ClosePuzzle() => PuzzleOpen = false;

        private void CompleteCampaignTask(TrainingCampaign.Task task)
        {
            if (!Campaign.TryInteract(task.Station, Puzzle)) return;
            Puzzle = null;
            PuzzleOpen = false;
            if (task.Action == CampaignAction.Exit || task.Action == CampaignAction.Return)
            {
                lastSecond = (int)SuitLimit;
                PlacePlayer(Outside);
            }
            ApplyMissionState();
            Report(task.Result, Finished ? finishTone : actionTone);
        }

        public void ChooseWire(int choice)
        {
            if (!WiringOpen || Mission.Step != MissionStep.Repair || choice < 0 || choice >= DayOneSimulation.WireCount)
                return;

            if (SelectedPlug < 0)
            {
                if ((Mission.ConnectedWires & (1 << choice)) != 0) return;
                SelectedPlug = choice;
                Report("Now choose the matching socket.", actionTone);
                return;
            }

            ConnectWire(SelectedPlug, choice);
        }

        public void ConnectWire(int plug, int socket)
        {
            if (!WiringOpen || Mission.Step != MissionStep.Repair) return;

            bool matched = Mission.TryConnect(plug, socket);
            if (matched && connectorClick != null) audioSource.PlayOneShot(connectorClick);
            SelectedPlug = -1;
            if (Mission.HeaterOn)
            {
                CloseWiring();
                Report("Heat restored. The heater needs power from the battery.", finishTone);
            }
            else if (matched)
                Report("Wire connected. Keep matching the remaining plugs.", actionTone);
            else
                Report("That socket is a different shape. Try the other one.", warningTone);
            ApplyMissionState();
        }

        public void CloseWiring()
        {
            SelectedPlug = -1;
            WiringOpen = false;
        }

        public void RestartDay()
        {
            advanceRequested = false;
            Puzzle = null;
            PuzzleOpen = false;
            if (Campaign == null) Mission = new DayOneSimulation();
            else Campaign.Restart();
            CloseWiring();
            PlacePlayer(false);
            ApplyMissionState();
            Feedback = Campaign?.Current.Briefing ?? "The habitat is getting cold. Bring the spare battery inside.";
        }

        public void RequestNextDay()
        {
            if (Finished && DayNumber < TrainingCampaign.LastDay) advanceRequested = true;
        }

        public void RestartMission()
        {
            advanceRequested = false;
            Campaign = null;
            RestartDay();
        }

        private void AdvanceDay()
        {
            if (!Finished || DayNumber == TrainingCampaign.LastDay) return;
            if (Campaign == null) Campaign = new TrainingCampaign(Mission.Water, Mission.Health);
            else Campaign.Advance();
            RestartDay();
        }

        private Transform Locate(Station station)
        {
            if (station == Station.Airlock) return Outside ? outsideAirlock : insideAirlock;
            return campaignStations[(int)station];
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
            Vector3 facing = view.position - spawn.position;
            facing.y = 0;
            player.transform.SetPositionAndRotation(spawn.position, Quaternion.LookRotation(facing));
            player.enabled = true;
            if (cameraView != null && cameraView != view) hud.FadeFromAirlock();
            cameraView = view;
            cameraOffset = Vector3.zero;
            sceneCamera.transform.SetPositionAndRotation(view.position, view.rotation);
            sceneCamera.orthographicSize = outside ? 6.55f : 5.6f;
            ResetMotion();
        }

        private void ResetMotion()
        {
            velocity = Vector3.zero;
            fallSpeed = stride = gait = 0f;
            PoseCadet();
        }

        private void ApplyMissionState()
        {
            outsideBattery.SetActive(Campaign == null && Mission.Step <= MissionStep.Collect);
            carriedBattery.SetActive(Campaign == null && (Mission.Step == MissionStep.Return || Mission.Step == MissionStep.Dock));
            dockedBattery.SetActive(Mission.PowerRestored);
            heaterLight.SetActive(Mission.HeaterOn);
            if (!Mission.HeaterOn && heaterGlow != null)
                heaterGlow.intensity = warmup = 0f;
            if (campaignStations != null && campaignStations.Length > 0)
            {
                for (int i = 0; i < campaignStations.Length; i++)
                {
                    if (campaignStations[i] == null || i == (int)Station.Dock || i == (int)Station.Water) continue;
                    Station station = (Station)i;
                    bool visible = station != Station.Sample ||
                        (Campaign != null && System.Array.Exists(Campaign.Current.Tasks, task => task.Station == station));
                    if (station == Station.Sample && Campaign?.CarryingSample == true) visible = false;
                    campaignStations[i].gameObject.SetActive(visible);
                }
                carriedSample.SetActive(Campaign?.CarryingSample == true);
                storedSample.SetActive(Campaign?.SampleStored == true);
                solarStatus.SetActive(DayNumber > 2 || (DayNumber == 2 && Campaign.Complete));
            }
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
            thirdKey?.Dispose();
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
