using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem.UI;

namespace LunaRangers.DayOne
{
    public sealed class DayOneHud : MonoBehaviour
    {
        private static readonly Color Ink = new Color32(14, 25, 44, 249);
        private static readonly Color Surface = new Color32(27, 44, 66, 255);
        private static readonly Color Track = new Color32(42, 58, 78, 255);
        private static readonly Color White = new Color32(243, 248, 255, 255);
        private static readonly Color Muted = new Color32(165, 187, 210, 255);
        private static readonly Color Cyan = new Color32(101, 224, 238, 255);
        private static readonly Color Amber = new Color32(255, 193, 89, 255);
        private static readonly Color Green = new Color32(130, 226, 169, 255);
        private static readonly Color Danger = new Color32(255, 152, 128, 255);
        private static readonly string[] Tasks =
        {
            "Step outside", "Pick up the spare battery", "Return to the habitat", "Dock the battery", "Reconnect the heater wires"
        };
        private static readonly string[] ResourcesNames = { "Suit oxygen", "Water reserve", "Cadet health" };
        private static readonly string[] WireShapes = { "Circle", "Triangle", "Square" };

        private Font font, semibold;
        private Sprite rounded;
        private UnityEngine.UI.Text[] checklist, taskNumbers, meterValues;
        private UnityEngine.UI.Image[] taskRows;
        private RectTransform[] meterFills;
        private UnityEngine.UI.Text timer, feedback, controls, prompt, actionKey, wireTip, outcomeTitle, outcomeBody;
        private UnityEngine.UI.Button interactionButton;
        private UnityEngine.UI.Button[] plugButtons, socketButtons;
        private UnityEngine.UI.Text[] plugLabels;
        private HeaterCable[] wireLinks;
        private RectTransform wiring, outcome, objective, targetDot, goals, resources, message;
        private UnityEngine.UI.Text objectiveLabel, dayTitle, dayNumber, nextLabel, retryLabel, location;
        private UnityEngine.UI.Button nextDay, retry;
        private UnityEngine.UI.Image airlockFade;
        private int? dragPointer;
        private RectTransform puzzleShade;
        private UnityEngine.UI.Text puzzleTitle, puzzleInstructions, puzzleReading, puzzleFeedback;
        private UnityEngine.UI.Button[] puzzleButtons;
        private UnityEngine.UI.Text[] puzzleLabels;
        private RectTransform[,] pipeArms;
        private bool showPuzzleHint;

        public void Build(DayOneLevel level)
        {
            font = Resources.Load<Font>("HUD/Fredoka-Regular") ?? Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            semibold = Resources.Load<Font>("HUD/Fredoka-Semibold") ?? font;
            rounded = CreateRoundedSprite();
            var canvasObject = new GameObject("Mission HUD", typeof(Canvas), typeof(UnityEngine.UI.CanvasScaler), typeof(UnityEngine.UI.GraphicRaycaster));
            canvasObject.transform.SetParent(transform, false);
            canvasObject.GetComponent<Canvas>().renderMode = RenderMode.ScreenSpaceOverlay;
            var scaler = canvasObject.GetComponent<UnityEngine.UI.CanvasScaler>();
            scaler.uiScaleMode = UnityEngine.UI.CanvasScaler.ScaleMode.ScaleWithScreenSize;
            scaler.referenceResolution = new Vector2(1280, 720);
            scaler.screenMatchMode = UnityEngine.UI.CanvasScaler.ScreenMatchMode.Expand;
            var root = (RectTransform)canvasObject.transform;
            var events = new GameObject("Day 1 input", typeof(EventSystem), typeof(InputSystemUIInputModule));
            events.transform.SetParent(transform, false);

            var topLeft = new Vector2(0f, 1f);
            var topRight = Vector2.one;
            var bottom = new Vector2(.5f, 0f);
            var center = new Vector2(.5f, .5f);
            targetDot = Panel(root, "Target marker", center, center, Vector2.zero, new Vector2(14, 14));
            targetDot.GetComponent<UnityEngine.UI.Image>().color = Amber;
            Panel(targetDot, "Marker center", center, center, Vector2.zero, new Vector2(6, 6))
                .GetComponent<UnityEngine.UI.Image>().color = Ink;
            objective = Panel(root, "Current objective", center, center, Vector2.zero, new Vector2(172, 32));
            objectiveLabel = Label(objective, "", 16, Amber, 6, 0, 160, 32, true);
            objectiveLabel.alignment = TextAnchor.MiddleCenter;
            objective.gameObject.SetActive(false);
            targetDot.gameObject.SetActive(false);
            var locationBadge = Panel(root, "Current location", new Vector2(.5f, 1), new Vector2(.5f, 1),
                new Vector2(0, -22), new Vector2(174, 30));
            location = Label(locationBadge, "", 15, White, 6, 0, 162, 30, true);
            location.alignment = TextAnchor.MiddleCenter;
            goals = Panel(root, "Mission objectives", topLeft, topLeft, new Vector2(22, -22), new Vector2(303, 245));
            dayNumber = Label(goals, "", 14, Cyan, 18, -12, 267, 23, true);
            dayTitle = Label(goals, "", 25, White, 18, -36, 267, 33, true);
            checklist = new UnityEngine.UI.Text[Tasks.Length];
            taskNumbers = new UnityEngine.UI.Text[Tasks.Length];
            taskRows = new UnityEngine.UI.Image[Tasks.Length];
            for (int i = 0; i < Tasks.Length; i++)
            {
                var row = Panel(goals, "Objective " + (i + 1), topLeft, topLeft, new Vector2(12, -77 - i * 31), new Vector2(279, 28));
                taskRows[i] = row.GetComponent<UnityEngine.UI.Image>();
                taskNumbers[i] = Label(row, "", 14, Muted, 8, 0, 24, 28, true);
                taskNumbers[i].alignment = TextAnchor.MiddleCenter;
                checklist[i] = Label(row, Tasks[i], 16, White, 39, 0, 232, 28);
            }

            resources = Panel(root, "Crew status", topRight, topRight, new Vector2(-22, -22), new Vector2(210, 159));
            Label(resources, "CREW STATUS", 14, Cyan, 16, -10, 178, 22, true);
            meterValues = new UnityEngine.UI.Text[ResourcesNames.Length];
            meterFills = new RectTransform[ResourcesNames.Length];
            for (int i = 0; i < ResourcesNames.Length; i++)
            {
                int y = -38 - i * 37;
                Label(resources, ResourcesNames[i], 16, White, 16, y, 126, 21);
                meterValues[i] = Label(resources, "", 16, White, 140, y, 54, 21, true);
                meterValues[i].alignment = TextAnchor.MiddleRight;
                var track = Panel(resources, ResourcesNames[i] + " track", topLeft, topLeft, new Vector2(16, y - 25), new Vector2(178, 5));
                track.GetComponent<UnityEngine.UI.Image>().color = Track;
                meterFills[i] = Panel(track, "Fill", topLeft, topLeft, Vector2.zero, new Vector2(178, 5));
            }
            timer = Label(resources, "", 19, Amber, 16, -157, 178, 32, true);

            message = Panel(root, "Player guidance", bottom, bottom, new Vector2(0, 18), new Vector2(558, 117));
            interactionButton = MakeButton(message, "Interact", 12, -10, 534, level);
            interactionButton.onClick.AddListener(level.Interact);
            prompt = interactionButton.GetComponentInChildren<UnityEngine.UI.Text>();
            prompt.color = Ink;
            prompt.fontSize = 19;
            var key = Panel((RectTransform)interactionButton.transform, "Interaction key", topLeft, topLeft, new Vector2(10, -7), new Vector2(30, 29));
            actionKey = Label(key, "E", 17, White, 0, 0, 30, 29, true);
            actionKey.alignment = TextAnchor.MiddleCenter;
            feedback = Label(message, "", 17, White, 16, -55, 526, 46);
            feedback.alignment = TextAnchor.MiddleCenter;
            controls = Label(message, "WASD / arrows  Move     ·     E  Interact     ·     R  Restart day", 14, Muted, 16, -101, 526, 20);
            controls.alignment = TextAnchor.MiddleCenter;

            var shade = Panel(root, "Heater focus", center, center, Vector2.zero, Vector2.zero);
            shade.anchorMin = Vector2.zero;
            shade.anchorMax = Vector2.one;
            var shadeImage = shade.GetComponent<UnityEngine.UI.Image>();
            shadeImage.sprite = null;
            shadeImage.color = new Color32(3, 8, 16, 205);
            shadeImage.raycastTarget = true;
            wiring = Panel(shade, "Heater wiring", center, center, Vector2.zero, new Vector2(540, 398));
            var face = Place(wiring, "Panel face", center, center, Vector2.zero, wiring.sizeDelta)
                .gameObject.AddComponent<UnityEngine.UI.RawImage>();
            face.texture = Resources.Load<Texture2D>("Heater/Panel");
            face.color = new Color32(36, 55, 79, 110);
            face.raycastTarget = false;
            Label(wiring, "HEATER CONTROL", 14, Cyan, 24, -12, 492, 22, true);
            Label(wiring, "Match the wires", 30, White, 24, -34, 492, 38, true);
            wireTip = Label(wiring, "", 18, White, 24, -75, 492, 34);
            Label(wiring, "PLUGS", 13, Muted, 24, -121, 126, 22, true);
            Label(wiring, "SOCKETS", 13, Muted, 390, -121, 126, 22, true);
            plugButtons = new UnityEngine.UI.Button[DayOneSimulation.WireCount];
            socketButtons = new UnityEngine.UI.Button[DayOneSimulation.WireCount];
            plugLabels = new UnityEngine.UI.Text[DayOneSimulation.WireCount];
            wireLinks = new HeaterCable[DayOneSimulation.WireCount];
            for (int i = 0; i < plugButtons.Length; i++)
            {
                int choice = i;
                string shape = WireShapes[i];
                var tint = i == 0 ? Cyan : i == 1 ? Amber : Green;
                var link = Place(wiring, shape + " wire", center, center, Vector2.zero, wiring.sizeDelta);
                var cable = link.gameObject.AddComponent<HeaterCable>();
                cable.color = tint;
                cable.raycastTarget = false;
                wireLinks[i] = cable;
                plugButtons[i] = MakeButton(wiring, shape, 24, -152 - i * 61, 126, level, choice);
                socketButtons[i] = MakeButton(wiring, shape, 390, -152 - ((i + 1) % 3) * 61, 126, level, choice);
                plugLabels[i] = plugButtons[i].GetComponentInChildren<UnityEngine.UI.Text>();
                plugLabels[i].color = tint;
                socketButtons[i].GetComponentInChildren<UnityEngine.UI.Text>().color = tint;

                var trigger = plugButtons[i].gameObject.AddComponent<EventTrigger>();
                var begin = new EventTrigger.Entry { eventID = EventTriggerType.BeginDrag };
                begin.callback.AddListener(e => BeginWireDrag(level, choice, (PointerEventData)e));
                var drag = new EventTrigger.Entry { eventID = EventTriggerType.Drag };
                drag.callback.AddListener(e => MoveWireDrag(choice, (PointerEventData)e));
                var end = new EventTrigger.Entry { eventID = EventTriggerType.EndDrag };
                end.callback.AddListener(e => EndWireDrag(level, choice, (PointerEventData)e));
                trigger.triggers.Add(begin);
                trigger.triggers.Add(drag);
                trigger.triggers.Add(end);
            }
            var close = MakeButton(wiring, "Close  (Esc)", 24, -336, 126, level);
            close.onClick.AddListener(level.CloseWiring);

            BuildPuzzle(root, level);

            var outcomeShade = Panel(root, "Debrief focus", center, center, Vector2.zero, Vector2.zero);
            outcomeShade.anchorMin = Vector2.zero;
            outcomeShade.anchorMax = Vector2.one;
            var outcomeShadeImage = outcomeShade.GetComponent<UnityEngine.UI.Image>();
            outcomeShadeImage.sprite = null;
            outcomeShadeImage.color = new Color32(3, 8, 16, 155);
            outcomeShadeImage.raycastTarget = true;
            outcome = Panel(outcomeShade, "Day result", center, center, Vector2.zero, new Vector2(438, 200));
            Label(outcome, "MISSION DEBRIEF", 14, Cyan, 22, -13, 394, 20, true);
            outcomeTitle = Label(outcome, "", 29, White, 22, -35, 394, 41, true);
            outcomeBody = Label(outcome, "", 18, White, 22, -76, 394, 46);
            retry = MakeButton(outcome, "Restart day (R)", 22, -139, 186, level);
            retryLabel = retry.GetComponentInChildren<UnityEngine.UI.Text>();
            retry.onClick.AddListener(level.RestartDay);
            nextDay = MakeButton(outcome, "Next day", 218, -139, 198, level);
            nextLabel = nextDay.GetComponentInChildren<UnityEngine.UI.Text>();
            nextDay.targetGraphic.color = Amber;
            nextLabel.color = Ink;
            nextDay.onClick.AddListener(() =>
            {
                if (level.DayNumber == TrainingCampaign.LastDay) level.RestartMission();
                else level.RequestNextDay();
            });
            wiring.parent.gameObject.SetActive(false);
            outcomeShade.gameObject.SetActive(false);
            var transition = Panel(root, "Airlock transition", center, center, Vector2.zero, Vector2.zero);
            transition.anchorMin = Vector2.zero;
            transition.anchorMax = Vector2.one;
            airlockFade = transition.GetComponent<UnityEngine.UI.Image>();
            airlockFade.sprite = null;
            airlockFade.color = new Color32(8, 16, 27, 0);
        }

        public void FadeFromAirlock()
        {
            airlockFade.color = new Color32(8, 16, 27, 230);
        }

        public void FollowObjective(DayOneLevel level)
        {
            var tint = airlockFade.color;
            if (tint.a > 0f)
            {
                tint.a = Mathf.MoveTowards(tint.a, 0f, 4f * Time.unscaledDeltaTime);
                airlockFade.color = tint;
            }

            var target = level.Objective;
            bool show = target != null && !level.WiringOpen && !level.PuzzleOpen;
            targetDot.gameObject.SetActive(show);
            objective.gameObject.SetActive(show && !interactionButton.interactable);
            if (!show) return;

            Vector3 point = level.sceneCamera.WorldToScreenPoint(target.position + Vector3.up * .15f);
            var canvas = (RectTransform)objective.parent;
            if (RectTransformUtility.ScreenPointToLocalPointInRectangle(canvas, point, null, out var anchor))
            {
                targetDot.anchoredPosition = anchor;
                Vector2 badge = anchor + new Vector2(0, 32);
                Rect bounds = canvas.rect;
                badge.x = Mathf.Clamp(badge.x, bounds.xMin + 93f, bounds.xMax - 93f);
                badge.y = Mathf.Clamp(badge.y, bounds.yMin + 159f, bounds.yMax - 24f);
                if (badge.x - 86f < bounds.xMin + 331f)
                    badge.y = Mathf.Min(badge.y, bounds.yMax - goals.sizeDelta.y - 42f);
                if (badge.x + 86f > bounds.xMax - 238f)
                    badge.y = Mathf.Min(badge.y, bounds.yMax - resources.sizeDelta.y - 42f);
                objective.anchoredPosition = badge;
            }
            objectiveLabel.text = level.ObjectiveName;
        }

        public void Show(DayOneLevel level, string interaction)
        {
            DayOneSimulation mission = level.Mission;
            var campaign = level.Campaign;
            dayNumber.text = $"DAY {level.DayNumber} OF {TrainingCampaign.LastDay}";
            dayTitle.text = campaign?.Current.Title ?? "Restore heat";
            float x = level.player.transform.position.x;
            location.text = level.Outside ? (level.DayNumber == 6 ? "Excavation site" : "Lunar surface") :
                x < 75f ? "West workshop" : x > 85f ? "East lab" : "Crew habitat";
            int step = campaign?.Step ?? (int)mission.Step;
            int taskCount = campaign?.Current.Tasks.Length ?? Tasks.Length;
            goals.sizeDelta = new Vector2(303, 90 + taskCount * 31);
            for (int i = 0; i < checklist.Length; i++)
            {
                taskRows[i].gameObject.SetActive(i < taskCount);
                if (i >= taskCount) continue;
                bool complete = step > i && !level.NeedsRetry;
                bool current = step == i && !level.NeedsRetry;
                checklist[i].text = campaign == null ? Tasks[i] : campaign.Current.Tasks[i].Label;
                checklist[i].color = complete ? Green : current ? Amber : Muted;
                checklist[i].font = current ? semibold : font;
                taskNumbers[i].text = complete ? "OK" : (i + 1).ToString();
                taskNumbers[i].color = checklist[i].color;
                taskRows[i].color = current ? Surface : Color.clear;
            }

            int oxygen = Mathf.CeilToInt(level.SecondsLeft / level.SuitLimit * 100f);
            SetMeter(0, oxygen, oxygen <= 30 ? Danger : Cyan);
            SetMeter(1, level.Water, new Color32(139, 180, 255, 255));
            SetMeter(2, level.Health, level.Health <= 40 ? Danger : Green);
            resources.sizeDelta = new Vector2(210, level.Outside ? 198 : 159);
            timer.gameObject.SetActive(level.Outside);
            timer.text = level.Outside ? $"Return in {Mathf.CeilToInt(level.SecondsLeft)} s" : "";
            timer.color = level.SecondsLeft <= 3f ? Danger : Amber;
            bool canInteract = interaction.StartsWith("E  ", System.StringComparison.Ordinal);
            bool hasPrompt = interaction.Length > 0;
            prompt.text = canInteract ? interaction.Substring(3) : interaction;
            prompt.color = canInteract ? Ink : Amber;
            prompt.rectTransform.anchoredPosition = new Vector2(canInteract ? 52 : 12, 0);
            prompt.rectTransform.sizeDelta = new Vector2(canInteract ? 470 : 510, 43);
            interactionButton.gameObject.SetActive(hasPrompt);
            interactionButton.interactable = canInteract;
            interactionButton.targetGraphic.color = canInteract ? Amber : Surface;
            actionKey.transform.parent.gameObject.SetActive(canInteract);
            message.sizeDelta = new Vector2(558, hasPrompt ? 129 : 84);
            feedback.rectTransform.anchoredPosition = new Vector2(16, hasPrompt ? -55 : -10);
            controls.rectTransform.anchoredPosition = new Vector2(16, hasPrompt ? -101 : -56);
            feedback.text = level.Feedback;
            message.gameObject.SetActive(!level.WiringOpen && !level.PuzzleOpen && !level.Finished && !level.NeedsRetry);
            ShowPuzzle(level);

            wiring.parent.gameObject.SetActive(level.WiringOpen);
            if (level.WiringOpen)
            {
                wireTip.text = level.SelectedPlug < 0
                    ? "Drag each plug to the socket with the same shape."
                    : "Select the socket with the same shape.";
                if (level.Feedback.StartsWith("That socket", System.StringComparison.Ordinal) ||
                    level.Feedback.StartsWith("Wire connected", System.StringComparison.Ordinal))
                    wireTip.text = level.Feedback;
                for (int i = 0; i < plugButtons.Length; i++)
                {
                    bool matched = (mission.ConnectedWires & (1 << i)) != 0;
                    string name = WireShapes[i];
                    if (dragPointer == null)
                    {
                        wireLinks[i].gameObject.SetActive(matched);
                        if (matched)
                            wireLinks[i].SetEnds(ConnectorEdge(plugButtons[i], true), ConnectorEdge(socketButtons[i], false));
                    }
                    plugLabels[i].text = matched ? name + "  OK" : name;
                    plugButtons[i].interactable = !matched && level.SelectedPlug < 0;
                    socketButtons[i].interactable = !matched && level.SelectedPlug >= 0;
                }
            }
            else dragPointer = null;

            bool finalDay = level.DayNumber == TrainingCampaign.LastDay;
            outcome.parent.gameObject.SetActive(level.Finished || level.NeedsRetry);
            outcomeTitle.text = level.Finished ? (finalDay ? "Mission complete" : $"Day {level.DayNumber} complete") : "Try this day again";
            outcomeBody.text = level.Finished
                ? campaign?.Current.Debrief ?? "Heat is back on. The spare battery powers the heater."
                : "Your suit ran out of time. Restart the day and head back sooner.";
            retryLabel.text = $"Restart Day {level.DayNumber}  (R)";
            nextDay.gameObject.SetActive(level.Finished);
            nextLabel.text = finalDay ? "Replay mission" : $"Start Day {level.DayNumber + 1}";
        }

        private void BuildPuzzle(RectTransform root, DayOneLevel level)
        {
            var center = new Vector2(.5f, .5f);
            var topLeft = new Vector2(0f, 1f);
            puzzleShade = Panel(root, "Puzzle focus", center, center, Vector2.zero, Vector2.zero);
            puzzleShade.anchorMin = Vector2.zero;
            puzzleShade.anchorMax = Vector2.one;
            var shade = puzzleShade.GetComponent<UnityEngine.UI.Image>();
            shade.sprite = null;
            shade.color = new Color32(3, 8, 16, 205);
            shade.raycastTarget = true;
            var board = Panel(puzzleShade, "Challenge board", center, center, Vector2.zero, new Vector2(666, 460));
            puzzleTitle = Label(board, "", 31, White, 24, -16, 618, 42, true);
            puzzleInstructions = Label(board, "", 19, White, 24, -60, 618, 49);
            puzzleReading = Label(board, "", 18, Cyan, 24, -113, 618, 29, true);
            puzzleFeedback = Label(board, "", 17, Amber, 24, -357, 618, 44);
            puzzleButtons = new UnityEngine.UI.Button[12];
            puzzleLabels = new UnityEngine.UI.Text[puzzleButtons.Length];
            pipeArms = new RectTransform[9, 4];
            for (int i = 0; i < puzzleButtons.Length; i++)
            {
                int slot = i;
                puzzleButtons[i] = MakeButton(board, "Option " + (i + 1), 24, -150, 198, level);
                puzzleButtons[i].onClick.AddListener(() => { showPuzzleHint = false; level.PressPuzzle(slot); });
                puzzleLabels[i] = puzzleButtons[i].GetComponentInChildren<UnityEngine.UI.Text>();
                puzzleLabels[i].alignment = TextAnchor.MiddleCenter;
                if (i >= 9) continue;
                for (int d = 0; d < 4; d++)
                {
                    bool vertical = d % 2 == 0;
                    Vector2 direction = d == 0 ? Vector2.up : d == 1 ? Vector2.right : d == 2 ? Vector2.down : Vector2.left;
                    var arm = Place((RectTransform)puzzleButtons[i].transform, "Pipe end", center, center,
                        new Vector2(54, 0) + direction * 12f, vertical ? new Vector2(7, 28) : new Vector2(28, 7));
                    var line = arm.gameObject.AddComponent<UnityEngine.UI.Image>();
                    line.color = Cyan;
                    line.raycastTarget = false;
                    pipeArms[i, d] = arm;
                }
            }
            MakeButton(board, "Close  (Esc)", 24, -403, 136, level).onClick.AddListener(level.ClosePuzzle);
            MakeButton(board, "Show hint", 506, -403, 136, level).onClick.AddListener(() => showPuzzleHint = !showPuzzleHint);
            puzzleShade.gameObject.SetActive(false);
        }

        private void ShowPuzzle(DayOneLevel level)
        {
            puzzleShade.gameObject.SetActive(level.PuzzleOpen);
            if (!level.PuzzleOpen) { showPuzzleHint = false; return; }
            var puzzle = level.Puzzle;
            puzzleTitle.text = puzzle.Title;
            puzzleInstructions.text = puzzle.Instructions;
            puzzleReading.text = level.Outside ? $"Return in {Mathf.CeilToInt(level.SecondsLeft)} s   |   {puzzle.Reading}" : puzzle.Reading;
            puzzleReading.color = level.Outside && level.SecondsLeft <= 5f ? Danger : Cyan;
            puzzleFeedback.text = showPuzzleHint ? puzzle.Hint : puzzle.Feedback;
            for (int i = 0; i < puzzleButtons.Length; i++)
            {
                var button = puzzleButtons[i];
                button.gameObject.SetActive(i < puzzle.Count);
                if (i >= puzzle.Count) continue;
                var rect = (RectTransform)button.transform;
                int top = puzzle.IsGrid ? 152 : 168;
                rect.anchoredPosition = new Vector2(24 + i % 3 * 210, -top - i / 3 * 53);
                var text = puzzleLabels[i];
                text.text = puzzle.Label(i);
                text.color = puzzle.IsActive(i) ? Cyan : White;
                button.targetGraphic.color = puzzle.IsActive(i) ? new Color32(40, 83, 106, 255) : Surface;
                int pipe = puzzle.Pipe(i);
                if (i < 9)
                    for (int d = 0; d < 4; d++) pipeArms[i, d].gameObject.SetActive((pipe & (1 << d)) != 0);
                text.alignment = pipe != 0 ? TextAnchor.MiddleLeft : TextAnchor.MiddleCenter;
                if (pipe != 0) text.text = (i + 1) + "   " + text.text;
            }
        }

        private void SetMeter(int index, int percent, Color tint)
        {
            meterValues[index].text = $"{percent}%";
            meterFills[index].sizeDelta = new Vector2(178f * Mathf.Clamp01(percent / 100f), 5);
            meterFills[index].GetComponent<UnityEngine.UI.Image>().color = tint;
        }

        private void BeginWireDrag(DayOneLevel level, int plug, PointerEventData pointer)
        {
            if (dragPointer != null || !level.WiringOpen || pointer.button != PointerEventData.InputButton.Left ||
                !plugButtons[plug].interactable) return;

            dragPointer = pointer.pointerId;
            pointer.eligibleForClick = false;
            wireLinks[plug].gameObject.SetActive(true);
            MoveWireDrag(plug, pointer);
        }

        private void MoveWireDrag(int plug, PointerEventData pointer)
        {
            if (dragPointer != pointer.pointerId) return;
            if (RectTransformUtility.ScreenPointToLocalPointInRectangle(wiring, pointer.position, pointer.pressEventCamera, out var end))
                wireLinks[plug].SetEnds(ConnectorEdge(plugButtons[plug], true), end);
        }

        private void EndWireDrag(DayOneLevel level, int plug, PointerEventData pointer)
        {
            if (dragPointer != pointer.pointerId) return;
            dragPointer = null;
            for (int socket = 0; socket < socketButtons.Length; socket++)
            {
                if (!RectTransformUtility.RectangleContainsScreenPoint((RectTransform)socketButtons[socket].transform,
                    pointer.position, pointer.pressEventCamera)) continue;
                level.ConnectWire(plug, socket);
                break;
            }
        }

        private Vector2 ConnectorEdge(UnityEngine.UI.Button button, bool fromPlug)
        {
            var rect = (RectTransform)button.transform;
            var edge = new Vector2(fromPlug ? rect.rect.xMax : rect.rect.xMin, rect.rect.center.y);
            return wiring.InverseTransformPoint(rect.TransformPoint(edge));
        }

        private RectTransform Panel(RectTransform parent, string name, Vector2 anchor, Vector2 pivot, Vector2 position, Vector2 size)
        {
            var rect = Place(parent, name, anchor, pivot, position, size);
            var background = rect.gameObject.AddComponent<UnityEngine.UI.Image>();
            background.sprite = rounded;
            background.type = UnityEngine.UI.Image.Type.Sliced;
            background.color = Ink;
            background.raycastTarget = false;
            return rect;
        }

        private UnityEngine.UI.Text Label(RectTransform parent, string value, int size, Color color, int x, int y, int width, int height, bool bold = false)
        {
            var topLeft = new Vector2(0, 1);
            var rect = Place(parent, value, topLeft, topLeft, new Vector2(x, y), new Vector2(width, height));
            var text = rect.gameObject.AddComponent<UnityEngine.UI.Text>();
            text.font = bold ? semibold : font;
            text.fontSize = size;
            text.color = color;
            text.text = value;
            text.alignment = TextAnchor.MiddleLeft;
            text.raycastTarget = false;
            return text;
        }

        private UnityEngine.UI.Button MakeButton(RectTransform parent, string title, int x, int y, int width, DayOneLevel level, int wire = -1)
        {
            var topLeft = new Vector2(0, 1);
            var rect = Panel(parent, title, topLeft, topLeft, new Vector2(x, y), new Vector2(width, 43));
            var image = rect.GetComponent<UnityEngine.UI.Image>();
            image.color = Surface;
            image.raycastTarget = true;
            var button = rect.gameObject.AddComponent<UnityEngine.UI.Button>();
            button.targetGraphic = image;
            var colors = button.colors;
            colors.normalColor = Color.white;
            colors.highlightedColor = new Color32(220, 234, 255, 255);
            colors.selectedColor = colors.highlightedColor;
            colors.disabledColor = new Color32(255, 255, 255, 170);
            button.colors = colors;
            Label(rect, title, 16, White, 12, 0, width - 24, 43, true);
            if (wire >= 0) button.onClick.AddListener(() => level.ChooseWire(wire));
            return button;
        }

        private static Sprite CreateRoundedSprite()
        {
            const int size = 32;
            const int radius = 10;
            var texture = new Texture2D(size, size, TextureFormat.RGBA32, false);
            var pixels = new Color32[size * size];
            for (int y = 0; y < size; y++)
            for (int x = 0; x < size; x++)
            {
                float dx = Mathf.Max(radius - Mathf.Min(x + .5f, size - x - .5f), 0f);
                float dy = Mathf.Max(radius - Mathf.Min(y + .5f, size - y - .5f), 0f);
                byte alpha = (byte)(Mathf.Clamp01(radius + .5f - Mathf.Sqrt(dx * dx + dy * dy)) * 255);
                pixels[y * size + x] = new Color32(255, 255, 255, alpha);
            }
            texture.SetPixels32(pixels);
            texture.Apply(false, true);
            return Sprite.Create(texture, new Rect(0, 0, size, size), new Vector2(.5f, .5f), 100f, 0,
                SpriteMeshType.FullRect, new Vector4(radius, radius, radius, radius));
        }

        private static RectTransform Place(RectTransform parent, string name, Vector2 anchor, Vector2 pivot, Vector2 position, Vector2 size)
        {
            var rect = new GameObject(name, typeof(RectTransform)).GetComponent<RectTransform>();
            rect.SetParent(parent, false);
            rect.anchorMin = anchor;
            rect.anchorMax = anchor;
            rect.pivot = pivot;
            rect.anchoredPosition = position;
            rect.sizeDelta = size;
            return rect;
        }
    }
}
