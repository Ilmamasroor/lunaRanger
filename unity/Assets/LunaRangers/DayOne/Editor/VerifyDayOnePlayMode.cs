using System;
using System.Collections;
using System.Collections.Generic;
using LunaRangers.DayOne;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
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

        yield return Tap(keyboard, Key.E);
        Require(level.Mission.Outside && level.Mission.SecondsLeft <= DayOneSimulation.SuitLimitSeconds, "Airlock failed to start the countdown.");
        yield return new WaitForSeconds(1f);
        Require(level.Mission.SuitOxygen < 100, "Oxygen did not drain during movement phase.");
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
        yield return Tap(keyboard, Key.E);
        Require(level.Mission.PowerRestored && level.dockedBattery.activeSelf, "Battery dock did not restore power.");
        yield return Walk(level, keyboard, level.heater.position + Vector3.back * .9f);
        yield return Tap(keyboard, Key.E);
        Require(level.WiringOpen, "The heater's wiring panel did not open.");
        yield return Tap(keyboard, Key.Digit1);
        yield return Tap(keyboard, Key.Digit2);
        Require(level.Mission.ConnectedWires == 0 && level.WiringOpen, "Wrong socket was accepted.");
        yield return Tap(keyboard, Key.Digit1);
        yield return Tap(keyboard, Key.Digit1);
        Require(level.Mission.ConnectedWires == 1 && level.WiringOpen, "First match did not remain visible while the next wire was pending.");
        yield return Tap(keyboard, Key.Digit2);
        yield return Tap(keyboard, Key.Digit2);
        Require(level.Mission.HeaterOn && level.heaterLight.activeSelf && !level.WiringOpen, "Both connectors did not complete Day 1.");
        yield return Tap(keyboard, Key.R);
        Require(level.Mission.Step == MissionStep.Exit && !level.heaterLight.activeSelf, "Restart did not reset the scene.");
    }

    private static IEnumerator Walk(DayOneLevel level, Keyboard keyboard, Vector3 target)
    {
        float deadline = Time.time + 4f;
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
