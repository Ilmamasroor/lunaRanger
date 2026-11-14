using System;
using System.IO;
using System.Linq;
using LunaRangers.DayOne;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEditor.SceneManagement;
using UnityEngine;

public static class CreateDayOneLevel
{
    private const string Outpost = "Assets/TechnicalResearch/LunaRangersOutpost.unity";
    private const string ScenePath = "Assets/LunaRangers/DayOne/DayOne.unity";
    private const string Art = "Assets/TechnicalResearch/LunaRangersArt/";

    [MenuItem("LunaRangers/Open Day 1")]
    public static void OpenDayOne()
    {
        if (EditorSceneManager.SaveCurrentModifiedScenesIfUserWantsTo())
            EditorSceneManager.OpenScene(ScenePath);
    }

    public static void CreateAndBuild()
    {
        VerifySimulation();
        if (!AssetDatabase.IsValidFolder("Assets/LunaRangers"))
            AssetDatabase.CreateFolder("Assets", "LunaRangers");
        if (!AssetDatabase.IsValidFolder("Assets/LunaRangers/DayOne"))
            AssetDatabase.CreateFolder("Assets/LunaRangers", "DayOne");

        if (!AssetDatabase.LoadAssetAtPath<SceneAsset>(ScenePath))
            Create();

        string[] args = Environment.GetCommandLineArgs();
        int outputArg = Array.IndexOf(args, "-dayOneOutput");
        if (outputArg < 0) return;
        string output = args[outputArg + 1];
        Directory.CreateDirectory(Path.GetDirectoryName(output));
        var report = BuildPipeline.BuildPlayer(new BuildPlayerOptions
        {
            scenes = new[] { ScenePath },
            target = BuildTarget.StandaloneWindows64,
            locationPathName = output,
            options = BuildOptions.None
        });
        if (report.summary.result != BuildResult.Succeeded)
            throw new BuildFailedException("Day 1 build: " + report.summary.result);
        Debug.Log("DAY_ONE_BUILD_PASSED " + report.summary.totalSize);
    }

    private static void Create()
    {
        if (!AssetDatabase.CopyAsset(Outpost, ScenePath))
            throw new InvalidOperationException("Could not create the Day 1 scene from the outpost.");
        var scene = EditorSceneManager.OpenScene(ScenePath);
        var probe = scene.GetRootGameObjects().Single(item => item.name == "ResearchProbe");
        UnityEngine.Object.DestroyImmediate(probe);
        var camera = scene.GetRootGameObjects().Single(item => item.CompareTag("MainCamera")).GetComponent<Camera>();
        camera.orthographic = true;
        camera.orthographicSize = 5.6f;
        camera.farClipPlane = 150f;

        var root = new GameObject("Day 1 training");
        var level = root.AddComponent<DayOneLevel>();
        level.hud = root.AddComponent<DayOneHud>();
        root.AddComponent<AudioSource>().playOnAwake = false;
        level.sceneCamera = camera;
        var parent = root.transform;
        var ivory = Material("Ivory hull");
        var trim = Material("Structural ribs");
        var dark = Material("Graphite supports");
        var orange = Material("Orange equipment");
        var blue = Material("Solar cells");

        var cadet = new GameObject("Cadet");
        cadet.transform.SetParent(parent);
        level.player = cadet.AddComponent<CharacterController>();
        level.player.height = 1.8f;
        level.player.center = new Vector3(0, .9f, 0);
        level.player.radius = .31f;
        level.player.minMoveDistance = 0f;
        var suit = scene.GetRootGameObjects().Single(item => item.name == "LunaRangers static astronaut");
        var renderers = suit.GetComponentsInChildren<Renderer>();
        Bounds suitBounds = renderers[0].bounds;
        foreach (var renderer in renderers) suitBounds.Encapsulate(renderer.bounds);
        suit.transform.SetParent(cadet.transform, true);
        suit.transform.position -= new Vector3(suitBounds.center.x, suitBounds.min.y, suitBounds.center.z);
        level.carriedBattery = Battery("Carried battery", cadet.transform, new Vector3(.45f, .9f, .1f), orange, dark, .62f);

        var exterior = Marker("Exterior tasks", parent, Vector3.zero);
        level.outsideAirlock = Marker("Outside hatch", exterior, new Vector3(-3.4f, 0, -1.7f));
        level.outsideStart = Marker("Outside spawn", exterior, new Vector3(-3.4f, .03f, -2.45f));
        level.batteryPickup = Marker("Battery pickup", exterior, new Vector3(-5.65f, 0, -4.12f));
        level.outsideBattery = Battery("Spare battery", level.batteryPickup, new Vector3(0, .32f, 0), orange, dark);
        Box("Battery location marker", level.batteryPickup, new Vector3(0, .015f, 0), new Vector3(1.2f, .03f, .9f), trim, false);
        Sign("BATTERY", level.outsideBattery.transform, new Vector3(0, .03f, -.242f), .092f);
        level.outsideView = View("Outside camera", exterior, new Vector3(5, 8.5f, -13), new Vector3(-2.9f, .75f, -2.7f));

        var room = Marker("Habitat interior", parent, new Vector3(80, 0, 0));
        Box("Floor", room, new Vector3(0, -.13f, 0), new Vector3(10, .26f, 10), trim);
        Box("Rear bulkhead", room, new Vector3(0, 1.65f, 4.8f), new Vector3(10, 3.3f, .3f), ivory);
        foreach (float x in new[] { -4.9f, 4.9f })
            Box("Side bulkhead", room, new Vector3(x, 1.2f, .4f), new Vector3(.3f, 2.4f, 8.8f), ivory);
        Box("Console shelf", room, new Vector3(0, 1.02f, 4.2f), new Vector3(4.2f, .16f, .8f), dark);
        Box("Airlock threshold", room, new Vector3(0, .025f, -3.7f), new Vector3(2.1f, .05f, 1f), orange, false);
        Sign("AIRLOCK", room, new Vector3(0, .24f, -3.87f), .16f);
        level.insideAirlock = Marker("Inside hatch", room, new Vector3(0, 0, -3.55f));
        level.insideStart = Marker("Inside spawn", room, new Vector3(0, .03f, -2.45f));
        level.insideView = View("Inside camera", room, new Vector3(0, 10.5f, -11.5f), new Vector3(0, .4f, .3f));

        level.dock = Marker("Battery dock", room, new Vector3(2.9f, 0, 1.25f));
        Box("Dock base", level.dock, new Vector3(0, .27f, 0), new Vector3(1.3f, .54f, 1.1f), dark);
        Box("Dock guide", level.dock, new Vector3(0, .57f, 0), new Vector3(1.07f, .08f, .85f), orange);
        Sign("BATTERY DOCK", level.dock, new Vector3(0, .3f, -.56f), .102f);
        level.dockedBattery = Battery("Docked battery", level.dock, new Vector3(0, .94f, 0), orange, dark);

        level.heater = Marker("Heater", room, new Vector3(-2.9f, 0, 1.25f));
        Box("Heater case", level.heater, new Vector3(0, .84f, 0), new Vector3(1.56f, 1.68f, .87f), orange);
        Box("Heater front", level.heater, new Vector3(0, .84f, -.45f), new Vector3(1.29f, 1.35f, .08f), ivory, false);
        for (int i = 0; i < 3; i++)
            Box("Heater grille", level.heater, new Vector3(0, .83f + i * .13f, -.504f), new Vector3(.93f, .055f, .04f), dark, false);
        Sign("HEATER", level.heater, new Vector3(0, .54f, -.51f), .14f);
        level.heaterLight = Box("Heat indicator", level.heater, new Vector3(0, 1.35f, -.5f), new Vector3(.35f, .12f, .06f), Material("Array status blue"), false);
        Box("Power conduit", room, new Vector3(0, .04f, 1.28f), new Vector3(5.2f, .08f, .13f), orange, false);

        level.waterStation = Marker("Water station", room, new Vector3(3.78f, 0, -2.18f));
        Box("Water station base", level.waterStation, new Vector3(0, .46f, 0), new Vector3(.85f, .92f, .7f), blue);
        Box("Water cartridge", level.waterStation, new Vector3(0, 1.18f, 0), new Vector3(.57f, .53f, .48f), trim);
        Sign("WATER", level.waterStation, new Vector3(0, .53f, -.36f), .12f);
        EditorSceneManager.MarkSceneDirty(scene);
        if (!EditorSceneManager.SaveScene(scene))
            throw new InvalidOperationException("Could not save the Day 1 scene.");
        Debug.Log("DAY_ONE_SCENE_SAVED " + ScenePath);
    }

    private static GameObject Battery(string name, Transform parent, Vector3 position, Material body, Material handle, float scale = 1f)
    {
        var battery = Marker(name, parent, position);
        battery.localScale = Vector3.one * scale;
        Box("Battery body", battery, Vector3.zero, new Vector3(.79f, .53f, .46f), body, false);
        Box("Carry handle", battery, new Vector3(0, .29f, 0), new Vector3(.37f, .11f, .17f), handle, false);
        return battery.gameObject;
    }

    private static Transform Marker(string name, Transform parent, Vector3 position)
    {
        var marker = new GameObject(name).transform;
        marker.SetParent(parent, false);
        marker.localPosition = position;
        return marker;
    }

    private static Transform View(string name, Transform parent, Vector3 position, Vector3 target)
    {
        var view = Marker(name, parent, position);
        view.LookAt(parent.TransformPoint(target));
        return view;
    }

    private static GameObject Box(string name, Transform parent, Vector3 position, Vector3 size, Material material, bool solid = true)
    {
        var box = GameObject.CreatePrimitive(PrimitiveType.Cube);
        box.name = name;
        box.transform.SetParent(parent, false);
        box.transform.localPosition = position;
        box.transform.localScale = size;
        box.GetComponent<MeshRenderer>().sharedMaterial = material;
        if (!solid) UnityEngine.Object.DestroyImmediate(box.GetComponent<BoxCollider>());
        return box;
    }

    private static void Sign(string title, Transform parent, Vector3 position, float size)
    {
        var sign = Marker(title + " sign", parent, position).gameObject.AddComponent<TextMesh>();
        sign.text = title;
        sign.anchor = TextAnchor.MiddleCenter;
        sign.alignment = TextAlignment.Center;
        sign.font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
        sign.GetComponent<MeshRenderer>().sharedMaterial = sign.font.material;
        sign.fontSize = 42;
        sign.characterSize = size;
        sign.color = title == "HEATER" ? new Color32(22, 43, 69, 255) : Color.white;
    }

    private static Material Material(string name)
    {
        var material = AssetDatabase.LoadAssetAtPath<Material>(Art + name + ".mat");
        if (!material) throw new InvalidOperationException("Missing outpost material " + name);
        return material;
    }

    private static void VerifySimulation()
    {
        var day = new DayOneSimulation();
        Require(!day.TryAdvance(MissionStep.Collect), "The player must exit before collecting.");
        Require(day.TryAdvance(MissionStep.Exit) && day.Outside, "Leaving starts the outdoor phase.");
        Require(!day.Tick(2f) && day.SuitOxygen == 80, "Suit oxygen follows the timer.");
        Require(day.Tick(8f) && day.Step == MissionStep.Exit && day.Health == 80, "Timeout restores the checkpoint and penalizes health.");
        Require(day.TryDrinkWater() && day.Health == 100 && day.Water == 90, "Water helps recover health indoors.");
        Require(!day.TryDrinkWater(), "Drinking at full health should not waste water.");
        Require(day.TryAdvance(MissionStep.Exit) && day.TryAdvance(MissionStep.Collect), "Battery can be picked up after retry.");
        Require(!day.TryDrinkWater() && day.TryAdvance(MissionStep.Return), "Water station is available indoors only.");
        Require(day.SuitOxygen == 100 && day.TryAdvance(MissionStep.Dock) && day.PowerRestored, "Docking restores power.");
        Require(!day.TryConnect(0, 1) && !day.HeaterOn, "Wrong connectors cannot start the heater.");
        Require(day.TryConnect(0, 0) && !day.TryConnect(0, 0) && !day.HeaterOn, "Matching a wire once cannot complete the task.");
        Require(day.TryConnect(1, 1) && day.HeaterOn, "Both matches restore heat.");
        var exhausted = new DayOneSimulation();
        for (int i = 0; i < 5; i++)
            Require(exhausted.TryAdvance(MissionStep.Exit) && exhausted.Tick(10f), "Exposure test did not reach timeout.");
        Require(exhausted.Step == MissionStep.Retry && exhausted.Health == 0 && !exhausted.TryDrinkWater(), "Depleted health requires a restart.");
        Debug.Log("DAY_ONE_SIMULATION_PASSED");
    }

    private static void Require(bool condition, string description)
    {
        if (!condition) throw new InvalidOperationException(description);
    }
}
