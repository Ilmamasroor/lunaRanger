using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem.UI;

namespace LunaRangers.DayOne
{
    public sealed class DayOneHud : MonoBehaviour
    {
        private static readonly Color Ink = new Color32(11, 22, 39, 240);
        private static readonly Color White = new Color32(243, 248, 255, 255);
        private static readonly Color Muted = new Color32(165, 187, 210, 255);
        private static readonly Color Cyan = new Color32(101, 224, 238, 255);
        private static readonly Color Amber = new Color32(255, 193, 89, 255);
        private static readonly Color Green = new Color32(130, 226, 169, 255);
        private static readonly Color Danger = new Color32(255, 152, 128, 255);
        private static readonly string[] Tasks =
        {
            "Exit the station", "Collect the battery", "Return inside", "Plug in the battery", "Connect the heater wires"
        };

        private Font font;
        private UnityEngine.UI.Text[] checklist;
        private UnityEngine.UI.Text meters, timer, feedback, prompt, wireTip, outcomeTitle, outcomeBody;
        private UnityEngine.UI.Button interactionButton;
        private UnityEngine.UI.Button[] plugButtons, socketButtons;
        private UnityEngine.UI.Text[] plugLabels;
        private GameObject[] wireLinks;
        private RectTransform wiring, outcome;

        public void Build(DayOneLevel level)
        {
            font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            var canvasObject = new GameObject("Day 1 HUD", typeof(Canvas), typeof(UnityEngine.UI.CanvasScaler), typeof(UnityEngine.UI.GraphicRaycaster));
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
            var goals = Panel(root, "Checklist", topLeft, topLeft, new Vector2(20, -20), new Vector2(294, 210));
            Label(goals, "DAY 1  /  RESTORE HEAT", 14, Cyan, 18, -10, 258, 29, true);
            Label(goals, "Checklist", 22, White, 18, -39, 258, 30, true);
            checklist = new UnityEngine.UI.Text[Tasks.Length];
            for (int i = 0; i < Tasks.Length; i++)
                checklist[i] = Label(goals, Tasks[i], 16, White, 18, -73 - i * 24, 258, 24);

            var resources = Panel(root, "Resources", topRight, topRight, new Vector2(-20, -20), new Vector2(224, 172));
            Label(resources, "SUIT & CREW", 14, Cyan, 16, -8, 192, 28, true);
            meters = Label(resources, "", 17, White, 16, -34, 192, 80);
            timer = Label(resources, "", 21, Amber, 16, -115, 192, 45, true);

            var message = Panel(root, "Player guidance", bottom, bottom, new Vector2(0, 18), new Vector2(620, 114));
            interactionButton = MakeButton(message, "Interact", 18, -6, 584, level);
            interactionButton.onClick.AddListener(level.Interact);
            prompt = interactionButton.GetComponentInChildren<UnityEngine.UI.Text>();
            prompt.color = Amber;
            feedback = Label(message, "", 16, White, 18, -49, 584, 34);
            Label(message, "WASD or arrows  Move       E  Interact       R  Restart", 13, Muted, 18, -84, 584, 23);

            wiring = Panel(root, "Heater wiring", center, center, Vector2.zero, new Vector2(434, 324));
            Label(wiring, "Match the connectors", 26, White, 22, -12, 390, 42, true);
            wireTip = Label(wiring, "", 16, Cyan, 22, -55, 390, 44);
            Label(wiring, "PLUGS", 13, Muted, 22, -104, 390, 24, true);
            Label(wiring, "SOCKETS", 13, Muted, 22, -179, 390, 24, true);
            plugButtons = new UnityEngine.UI.Button[2];
            socketButtons = new UnityEngine.UI.Button[2];
            plugLabels = new UnityEngine.UI.Text[2];
            wireLinks = new GameObject[2];
            for (int i = 0; i < 2; i++)
            {
                int choice = i;
                string shape = i == 0 ? "Circle" : "Triangle";
                int left = 22 + i * 198;
                var tint = i == 0 ? Cyan : Amber;
                var link = Place(wiring, shape + " wire", topLeft, topLeft, new Vector2(left + 92, -171), new Vector2(6, 32));
                var line = link.gameObject.AddComponent<UnityEngine.UI.Image>();
                line.color = tint;
                line.raycastTarget = false;
                wireLinks[i] = link.gameObject;
                plugButtons[i] = MakeButton(wiring, shape + " plug", left, -128, 190, level, choice);
                socketButtons[i] = MakeButton(wiring, shape + " socket", left, -203, 190, level, choice);
                plugLabels[i] = plugButtons[i].GetComponentInChildren<UnityEngine.UI.Text>();
                plugLabels[i].color = tint;
                socketButtons[i].GetComponentInChildren<UnityEngine.UI.Text>().color = tint;
            }
            var close = MakeButton(wiring, "Back  (Esc)", 22, -267, 190, level);
            close.onClick.AddListener(level.CloseWiring);

            outcome = Panel(root, "Day result", center, center, Vector2.zero, new Vector2(438, 188));
            outcomeTitle = Label(outcome, "", 28, Cyan, 22, -10, 394, 46, true);
            outcomeBody = Label(outcome, "", 17, White, 22, -58, 394, 54);
            var retry = MakeButton(outcome, "Restart Day 1  (R)", 22, -124, 215, level);
            retry.onClick.AddListener(level.RestartDay);
            wiring.gameObject.SetActive(false);
            outcome.gameObject.SetActive(false);
        }

        public void Show(DayOneLevel level, string interaction)
        {
            DayOneSimulation mission = level.Mission;
            for (int i = 0; i < checklist.Length; i++)
            {
                bool complete = (int)mission.Step > i && mission.Step != MissionStep.Retry;
                bool current = (int)mission.Step == i;
                checklist[i].text = (complete ? "[x]  " : current ? ">    " : "[ ]   ") + Tasks[i];
                checklist[i].color = complete ? Green : current ? Amber : Muted;
            }

            meters.text = $"Suit oxygen    {mission.SuitOxygen}%\nWater reserve  {mission.Water}%\nCadet health   {mission.Health}%";
            timer.text = mission.Outside ? $"SUIT TIMER   {Mathf.CeilToInt(mission.SecondsLeft):00}s" : "";
            timer.color = mission.SecondsLeft <= 3f ? Danger : Amber;
            prompt.text = interaction;
            interactionButton.gameObject.SetActive(interaction.Length > 0);
            interactionButton.interactable = interaction.StartsWith("E  ", System.StringComparison.Ordinal);
            feedback.text = level.Feedback;

            wiring.gameObject.SetActive(level.WiringOpen);
            if (level.WiringOpen)
            {
                wireTip.text = level.SelectedPlug < 0 ? "Choose a plug  (1 or 2)" : "Choose the socket with the same shape  (1 or 2)";
                for (int i = 0; i < 2; i++)
                {
                    bool matched = (mission.ConnectedWires & (1 << i)) != 0;
                    string name = i == 0 ? "Circle" : "Triangle";
                    wireLinks[i].SetActive(matched);
                    plugLabels[i].text = matched ? name + " connected" : name + " plug";
                    plugButtons[i].interactable = !matched && level.SelectedPlug < 0;
                    socketButtons[i].interactable = !matched && level.SelectedPlug >= 0;
                }
            }

            outcome.gameObject.SetActive(mission.Step >= MissionStep.Complete);
            outcomeTitle.text = mission.HeaterOn ? "DAY 1 COMPLETE" : "TRAINING PAUSED";
            outcomeBody.text = mission.HeaterOn ? "Heat restored. The heater needs power from the battery." : "Suit exposure depleted your health. Restart to try again.";
        }

        private static RectTransform Panel(RectTransform parent, string name, Vector2 anchor, Vector2 pivot, Vector2 position, Vector2 size)
        {
            var rect = Place(parent, name, anchor, pivot, position, size);
            var background = rect.gameObject.AddComponent<UnityEngine.UI.Image>();
            background.color = Ink;
            background.raycastTarget = false;
            return rect;
        }

        private UnityEngine.UI.Text Label(RectTransform parent, string value, int size, Color color, int x, int y, int width, int height, bool bold = false)
        {
            var topLeft = new Vector2(0, 1);
            var rect = Place(parent, value, topLeft, topLeft, new Vector2(x, y), new Vector2(width, height));
            var text = rect.gameObject.AddComponent<UnityEngine.UI.Text>();
            text.font = font;
            text.fontSize = size;
            text.fontStyle = bold ? FontStyle.Bold : FontStyle.Normal;
            text.color = color;
            text.text = value;
            text.alignment = TextAnchor.MiddleLeft;
            text.raycastTarget = false;
            return text;
        }

        private UnityEngine.UI.Button MakeButton(RectTransform parent, string title, int x, int y, int width, DayOneLevel level, int wire = -1)
        {
            var topLeft = new Vector2(0, 1);
            var rect = Place(parent, title, topLeft, topLeft, new Vector2(x, y), new Vector2(width, 43));
            var image = rect.gameObject.AddComponent<UnityEngine.UI.Image>();
            image.color = new Color32(47, 73, 104, 255);
            var button = rect.gameObject.AddComponent<UnityEngine.UI.Button>();
            button.targetGraphic = image;
            Label(rect, title, 16, White, 12, 0, width - 24, 43, true);
            if (wire >= 0) button.onClick.AddListener(() => level.ChooseWire(wire));
            return button;
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
