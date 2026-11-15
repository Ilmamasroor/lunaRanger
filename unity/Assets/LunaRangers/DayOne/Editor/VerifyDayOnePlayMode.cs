using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using LunaRangers.DayOne;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.InputSystem;
using UnityEngine.InputSystem.LowLevel;

[InitializeOnLoad]
public static class VerifyDayOnePlayMode
{
    private const string Running = "LunaRangers.VerifyDayOne";

    static VerifyDayOnePlayMode()
    {
        if (SessionState.GetBool(Running, false))
            EditorApplication.playModeStateChanged += OnPlayModeChanged;
    }

    public static void Run()
    {
        EditorSceneManager.OpenScene("Assets/LunaRangers/DayOne/DayOne.unity");
        SessionState.SetBool(Running, true);
        EditorApplication.playModeStateChanged -= OnPlayModeChanged;
        EditorApplication.playModeStateChanged += OnPlayModeChanged;
        EditorApplication.EnterPlaymode();
    }

    private static void OnPlayModeChanged(PlayModeStateChange state)
    {
        if (state != PlayModeStateChange.EnteredPlayMode) return;
        EditorApplication.delayCall += () =>
        {
            Application.runInBackground = true;
            Application.targetFrameRate = 60;
            var settings = UnityEngine.Object.Instantiate(InputSystem.settings);
            settings.editorInputBehaviorInPlayMode = InputSettings.EditorInputBehaviorInPlayMode.AllDeviceInputAlwaysGoesToGameView;
            settings.backgroundBehavior = InputSettings.BackgroundBehavior.IgnoreFocus;
            settings.updateMode = InputSettings.UpdateMode.ProcessEventsManually;
            InputSystem.settings = settings;
            var level = UnityEngine.Object.FindFirstObjectByType<DayOneLevel>();
            if (!level)
            {
                Finish(new InvalidOperationException("Day 1 scene did not load."));
                return;
            }
            var keyboard = InputSystem.AddDevice<Keyboard>();
            keyboard.MakeCurrent();
            level.StartCoroutine(RunAndReport(Play(level, keyboard), keyboard));
        };
    }

    private static IEnumerator RunAndReport(IEnumerator test, Keyboard keyboard)
    {
        var pending = new Stack<IEnumerator>();
        pending.Push(test);
        while (pending.Count > 0)
        {
            object next = null;
            try
            {
                var step = pending.Peek();
                if (step.MoveNext()) next = step.Current;
                else { pending.Pop(); continue; }
            }
            catch (Exception failure)
            {
                InputSystem.RemoveDevice(keyboard);
                Finish(failure);
                yield break;
            }

            if (next is IEnumerator child) pending.Push(child);
            else yield return next;
        }
        InputSystem.RemoveDevice(keyboard);
        Finish(null);
    }

    private static void Finish(Exception failure)
    {
        SessionState.EraseBool(Running);
        if (failure != null) Debug.LogException(failure);
        else Debug.Log("DAY_ONE_PLAYTHROUGH_PASSED");
        EditorApplication.Exit(failure == null ? 0 : 1);
    }

    private static IEnumerator Play(DayOneLevel level, Keyboard keyboard)
    {
        yield return null;
        int frame = Time.frameCount;
        yield return null;
        Require(Time.frameCount > frame && level.Mission.Step == MissionStep.Exit, "The playable scene did not start.");
        yield return new WaitForSeconds(.25f);
        Require(level.player.isGrounded, "The cadet did not settle on the habitat floor.");
        Require(level.cadetBody && level.leftBoot && level.rightBoot && level.leftArm && level.rightArm,
            "The animated cadet is missing parts.");
        Require(Mathf.Approximately(level.leftBoot.localPosition.z, level.rightBoot.localPosition.z),
            "The cadet did not start in an idle pose.");

        yield return Tap(keyboard, Key.E);
        Require(level.Mission.Outside && level.Mission.SecondsLeft <= DayOneSimulation.SuitLimitSeconds, "Airlock failed to start the countdown.");
        yield return new WaitForSeconds(1f);
        Require(level.player.isGrounded, "The cadet did not settle on the lunar surface.");
        Require(level.Mission.SuitOxygen < 100, "Oxygen did not drain during movement phase.");
        SetKeys(keyboard, Key.A);
        bool leftForward = false, rightForward = false;
        for (float elapsed = 0; elapsed < .45f; elapsed += Time.deltaTime)
        {
            yield return null;
            float difference = level.leftBoot.localPosition.z - level.rightBoot.localPosition.z;
            leftForward |= difference > .08f;
            rightForward |= difference < -.08f;
        }
        SetKeys(keyboard);
        Require(leftForward && rightForward, "The cadet did not alternate steps while walking.");
        yield return new WaitForSeconds(.25f);
        Require(Mathf.Abs(level.leftBoot.localPosition.z - level.rightBoot.localPosition.z) < .01f,
            "The cadet kept walking after stopping.");
        yield return new WaitForSeconds(9.2f);
        Require(level.Mission.Step == MissionStep.Exit && level.Mission.Health == 80 &&
            Vector3.Distance(level.player.transform.position, level.insideStart.position) < .1f, "Timeout failed to return the player indoors.");

        yield return Walk(level, keyboard, level.waterStation.position + Vector3.left * .8f);
        yield return Tap(keyboard, Key.E);
        Require(level.Mission.Water == 90 && level.Mission.Health == 100, "Water station did not restore health.");
        yield return Walk(level, keyboard, level.insideStart.position);
        yield return Tap(keyboard, Key.E);
        Require(level.Mission.Step == MissionStep.Collect, "Second exit failed.");
        yield return Walk(level, keyboard, level.batteryPickup.position);
        yield return Tap(keyboard, Key.E);
        Require(level.Mission.Step == MissionStep.Return && level.carriedBattery.activeSelf && !level.outsideBattery.activeSelf, "Battery pickup failed.");
        yield return Walk(level, keyboard, level.outsideStart.position);
        yield return Tap(keyboard, Key.E);
        Require(level.Mission.Step == MissionStep.Dock && level.Mission.SuitOxygen == 100, "Returning inside with the battery failed.");

        yield return Walk(level, keyboard, level.dock.position + Vector3.back * .9f);
        SetKeys(keyboard, Key.W);
        yield return new WaitForSeconds(.45f);
        SetKeys(keyboard);
        yield return new WaitForSeconds(.15f);
        var stopped = level.player.transform.position;
        yield return new WaitForSeconds(.2f);
        Require(stopped.z < level.dock.position.z - .6f && Vector3.Distance(stopped, level.player.transform.position) < .015f,
            "The cadet passed through the dock or continued sliding after input stopped.");
        yield return Tap(keyboard, Key.E);
        Require(level.Mission.PowerRestored && level.dockedBattery.activeSelf, "Battery dock did not restore power.");
        yield return Walk(level, keyboard, level.heater.position + Vector3.back * .9f);
        yield return Tap(keyboard, Key.E);
        Require(level.WiringOpen, "The heater's wiring panel did not open.");
        DragWire(level, 0, 1);
        yield return null;
        Require(level.Mission.ConnectedWires == 0 && level.WiringOpen, "Wrong socket was accepted.");
        DragWire(level, 0, null);
        yield return null;
        Require(level.Mission.ConnectedWires == 0 && level.SelectedPlug < 0, "Dropping outside the sockets did not cancel the drag.");
        yield return Tap(keyboard, Key.Digit1);
        yield return Tap(keyboard, Key.Digit1);
        Require(level.Mission.ConnectedWires == 1 && level.WiringOpen, "First match did not remain visible while the next wire was pending.");
        DragWire(level, 1, 1);
        yield return null;
        Require(!level.Mission.HeaterOn, "Two wires incorrectly completed the heater.");
        DragWire(level, 2, 2);
        yield return null;
        Require(level.Mission.HeaterOn && level.heaterLight.activeSelf && !level.WiringOpen, "All three wires did not complete Day 1.");
        yield return new WaitForSeconds(.4f);
        Require(level.heaterLight.GetComponentInChildren<Light>().intensity > 1f, "The repaired heater did not warm the habitat.");
        yield return Tap(keyboard, Key.R);
        Require(level.Mission.Step == MissionStep.Exit && !level.heaterLight.activeSelf, "Restart did not reset the scene.");
        level.RequestNextDay();
        yield return null;
        Require(level.Objective == level.insideAirlock, "An incomplete day could be skipped.");

        yield return Tap(keyboard, Key.E);
        yield return Walk(level, keyboard, level.batteryPickup.position);
        yield return Tap(keyboard, Key.E);
        yield return Walk(level, keyboard, level.outsideStart.position);
        yield return Tap(keyboard, Key.E);
        yield return Walk(level, keyboard, level.dock.position + Vector3.back * .9f);
        yield return Tap(keyboard, Key.E);
        yield return Walk(level, keyboard, level.heater.position + Vector3.back * .9f);
        yield return Tap(keyboard, Key.E);
        DragWire(level, 0, 0);
        yield return null;
        DragWire(level, 1, 1);
        yield return null;
        DragWire(level, 2, 2);
        yield return null;
        yield return Campaign(level, keyboard);
    }

    private static IEnumerator Campaign(DayOneLevel level, Keyboard keyboard)
    {
        string[][] stations =
        {
            new[] { "Power console" },
            new[] { "Filter valve", "Lab recycler" },
            new[] { "CO2 scrubber" },
            new[] { "Crew shelter" },
            new[] { "Suit station", "Inside hatch", "Moon rock", "Outside hatch" },
            new[] { "Sample locker", "Mission terminal" }
        };

        for (int day = 2; day <= 7; day++)
        {
            ButtonWithText(level, "Start Day " + day).onClick.Invoke();
            yield return null;
            yield return null;
            if (day == 5)
            {
                yield return Tap(keyboard, Key.E);
                Require(level.Objective.name == "Crew shelter", "The solar alert allowed an early departure.");
            }

            if (day == 6)
            {
                yield return UseStation("Suit station");
                yield return UseStation("Inside hatch");
                yield return UseStation("Moon rock", false);
                Require(!level.carriedSample.activeSelf && ButtonWithText(level, "Scan") != null,
                    "The dig phase granted a sample without excavation.");
                yield return new WaitForSeconds(25.1f);
                Require(level.Objective.name == "Suit station" && !level.carriedSample.activeSelf,
                    "An EVA timeout did not reset the sample run.");
            }

            foreach (string station in stations[day - 2])
                yield return UseStation(station);

            Require(level.Objective == null, "Day " + day + " did not complete.");
        }

        Require(level.storedSample.activeSelf, "The mission ended without storing a sample.");
        ButtonWithText(level, "Replay mission").onClick.Invoke();
        yield return null;
        Require(level.Objective == level.insideAirlock && !level.storedSample.activeSelf, "Mission replay did not reset Day 1.");
        Debug.Log("SEVEN_DAY_CAMPAIGN_PASSED");

        IEnumerator UseStation(string name, bool solve = true)
        {
            var station = level.Objective;
            Require(station != null && station.name == name, "Expected station " + name + ".");
            Vector3 approach = name switch
            {
                "Battery dock" => Vector3.back * .9f,
                "Water station" => Vector3.left * .8f,
                "Inside hatch" => Vector3.forward * .8f,
                "Outside hatch" => Vector3.back * .75f,
                _ => Vector3.zero
            };
            if (station.position.x > 60 && Zone(station.position.x) != Zone(level.player.transform.position.x))
            {
                yield return Walk(level, keyboard, new Vector3(level.player.transform.position.x, 0, -2.2f));
                yield return Walk(level, keyboard, new Vector3(Zone(station.position.x) * 10 + 80, 0, -2.2f));
            }
            if (name == "Mission terminal")
                yield return Walk(level, keyboard, new Vector3(80, 0, 3.45f));
            yield return Walk(level, keyboard, station.position + approach);
            yield return Tap(keyboard, Key.E);
            if (!solve) yield break;
            int[] inputs = name switch
            {
                "Power console" => new[] { 0, 1, 2, 3, 5, 3, 5 },
                "Filter valve" => new[] { 9, 0, 1, 2, 2, 2, 3, 5, 9 },
                "CO2 scrubber" => new[] { 0, 1, 2 },
                "Crew shelter" => new[] { 0, 1, 2, 4, 2, 4 },
                "Moon rock" => new[] { 9, 11, 4, 10, 0, 4, 4, 11, 4 },
                "Sample locker" => new[] { 0, 1, 2, 0 },
                _ => null
            };
            if (inputs == null) yield break;
            Require(level.Objective == station, "Opening " + name + " skipped its puzzle.");
            ButtonWithText(level, "Show hint").onClick.Invoke();
            yield return null;
            yield return Tap(keyboard, Key.Escape);
            Require(level.Objective == station, "Closing " + name + " completed its puzzle.");
            yield return Tap(keyboard, Key.E);
            for (int i = 0; i < inputs.Length; i++)
            {
                var button = level.hud.GetComponentsInChildren<UnityEngine.UI.Button>()
                    .Single(x => x.name == "Option " + (inputs[i] + 1));
                button.onClick.Invoke();
                yield return null;
                if (i < inputs.Length - 1)
                    Require(level.Objective == station, name + " accepted an incomplete solution.");
            }
            Require(level.Objective != station, name + " did not accept its valid solution.");
        }

        int Zone(float x) => x < 75 ? -1 : x > 85 ? 1 : 0;
    }

    private static UnityEngine.UI.Button ButtonWithText(DayOneLevel level, string label)
    {
        return level.hud.GetComponentsInChildren<UnityEngine.UI.Button>().Single(button =>
            button.GetComponentInChildren<UnityEngine.UI.Text>().text == label);
    }

    private static void DragWire(DayOneLevel level, int plug, int? socket)
    {
        var panel = level.hud.GetComponentsInChildren<RectTransform>().First(rect => rect.name == "Heater wiring");
        string[] shapes = { "Circle", "Triangle", "Square" };
        var buttons = panel.GetComponentsInChildren<UnityEngine.UI.Button>();
        var source = (RectTransform)buttons.First(button => button.name == shapes[plug]).transform;
        var target = socket.HasValue
            ? (RectTransform)buttons.Last(button => button.name == shapes[socket.Value]).transform
            : panel;
        var pointer = new PointerEventData(EventSystem.current) { button = PointerEventData.InputButton.Left };
        pointer.position = RectTransformUtility.WorldToScreenPoint(null, source.TransformPoint(source.rect.center));
        ExecuteEvents.Execute(source.gameObject, pointer, ExecuteEvents.beginDragHandler);
        pointer.position = RectTransformUtility.WorldToScreenPoint(null, target.TransformPoint(target.rect.center));
        ExecuteEvents.Execute(source.gameObject, pointer, ExecuteEvents.dragHandler);
        ExecuteEvents.Execute(source.gameObject, pointer, ExecuteEvents.endDragHandler);
    }

    private static IEnumerator Walk(DayOneLevel level, Keyboard keyboard, Vector3 target)
    {
        float deadline = Time.time + 7f;
        Vector3 right = Vector3.ProjectOnPlane(level.sceneCamera.transform.right, Vector3.up).normalized;
        Vector3 forward = Vector3.Cross(right, Vector3.up);
        while (true)
        {
            Vector3 difference = target - level.player.transform.position;
            difference.y = 0f;
            if (difference.sqrMagnitude < .14f) break;
            Require(Time.time < deadline, "Could not reach " + target + " from " + level.player.transform.position);
            var keys = new List<Key>(2);
            float horizontal = Vector3.Dot(difference, right);
            float vertical = Vector3.Dot(difference, forward);
            if (Mathf.Abs(horizontal) > .14f) keys.Add(horizontal > 0 ? Key.D : Key.A);
            if (Mathf.Abs(vertical) > .14f) keys.Add(vertical > 0 ? Key.W : Key.S);
            SetKeys(keyboard, keys.ToArray());
            yield return null;
        }
        SetKeys(keyboard);
        yield return null;
    }

    private static IEnumerator Tap(Keyboard keyboard, Key key)
    {
        SetKeys(keyboard, key);
        yield return null;
        SetKeys(keyboard);
        yield return null;
    }

    private static void SetKeys(Keyboard keyboard, params Key[] keys)
    {
        InputSystem.QueueStateEvent(keyboard, new KeyboardState(keys));
        InputSystem.Update();
        foreach (Key key in keys)
            Require(keyboard[key].isPressed, "Input System did not process the queued key " + key);
    }

    private static void Require(bool condition, string message)
    {
        if (!condition) throw new InvalidOperationException(message);
    }
}
