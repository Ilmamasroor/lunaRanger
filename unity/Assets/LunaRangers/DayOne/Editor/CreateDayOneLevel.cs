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

    public static void ApplyMissionRooms()
    {
        var scene = EditorSceneManager.OpenScene(ScenePath);
        var level = UnityEngine.Object.FindFirstObjectByType<DayOneLevel>();
        var waterPosition = new Vector3(3.78f, 0, -1.05f);
        if (level.hasAnnexes)
        {
            if (level.waterStation.localPosition != waterPosition)
            {
                level.waterStation.localPosition = waterPosition;
                EditorSceneManager.MarkSceneDirty(scene);
                if (!EditorSceneManager.SaveScene(scene)) throw new InvalidOperationException("Could not clear the east passage.");
            }
            return;
        }
        level.waterStation.localPosition = waterPosition;
        var room = level.insideStart.parent;
        var ivory = Material("Ivory hull");
        var dark = Material("Graphite supports");
        var blue = Material("Solar cells");
        var orange = Material("Orange equipment");
        var lamp = Material("Array status blue");
        var west = Marker("West Workshop", room, new Vector3(-10, 0, 0));
        var east = Marker("East Lab", room, new Vector3(10, 0, 0));

        foreach (Transform child in room)
            if (child.name == "Side bulkhead") child.gameObject.SetActive(false);
        foreach (int side in new[] { -1, 1 })
        {
            var bay = side < 0 ? west : east;
            var accent = side < 0 ? orange : blue;
            Box("Floor", bay, new Vector3(0, -.13f, 0), new Vector3(10, .26f, 10), dark);
            Box("Deck", bay, new Vector3(0, .011f, .3f), new Vector3(8.9f, .02f, 8.3f), accent, false);
            Box("Rear bulkhead", bay, new Vector3(0, 1.2f, 4.8f), new Vector3(10, 2.4f, .3f), ivory);
            Box("End bulkhead", bay, new Vector3(side * 4.85f, 1.15f, 0), new Vector3(.28f, 2.3f, 9.5f), ivory);
            Box("Partition", room, new Vector3(side * 5, 1.05f, 2.05f), new Vector3(.25f, 2.1f, 5.4f), ivory);
            Box("Partition", room, new Vector3(side * 5, .9f, -4.45f), new Vector3(.25f, 1.8f, 1.4f), ivory);
            Box("Passage threshold", room, new Vector3(side * 5, .023f, -2.2f), new Vector3(1.15f, .04f, 2.7f), lamp, false);
            for (int i = 0; i < 3; i++)
                Box("Deck seam", bay, new Vector3(0, .028f, i * 2.25f - 1.45f), new Vector3(8.7f, .01f, .065f), dark, false);
        }

        var stations = level.campaignStations;
        MoveStation(0, west, new Vector3(-1.8f, 0, 1.95f));
        for (int i = -1; i <= 1; i++)
            Box("Breaker stack", stations[0], new Vector3(i * .29f, 1.13f, .06f), new Vector3(.2f, .35f, .32f), lamp, false);
        MoveStation(6, west, new Vector3(-2.3f, 0, -1.15f));
        Box("Shield frame", stations[6], new Vector3(0, .75f, .5f), new Vector3(2.1f, 1.5f, .28f), dark, false);
        for (int i = 0; i < 3; i++)
            Box("Shield panel", stations[6], new Vector3((i - 1) * .58f, .8f, .31f), new Vector3(.45f, 1.08f, .12f), ivory, false);
        MoveStation(7, west, new Vector3(2.85f, 0, -2.3f));
        Box("Suit rack", stations[7], new Vector3(0, 1.05f, .42f), new Vector3(.75f, 2.1f, .18f), dark, false);
        SuitPart("Spare helmet", stations[7], new Vector3(0, 1.4f, .18f), new Vector3(.48f, .41f, .44f), ivory);

        MoveStation(2, east, new Vector3(-1.5f, 0, .8f));
        stations[3] = Marker("Lab recycler", east, new Vector3(2.1f, 0, .8f));
        SuitPart("Recycler reservoir", stations[3], new Vector3(0, .75f, 0), new Vector3(.82f, 1.5f, .82f), ivory, PrimitiveType.Capsule);
        Box("Water window", stations[3], new Vector3(0, .8f, -.4f), new Vector3(.42f, .69f, .11f), lamp, false);
        Box("Water pipe", east, new Vector3(.3f, .18f, .84f), new Vector3(3.1f, .25f, .25f), lamp, false);
        MoveStation(4, east, new Vector3(-1.1f, 0, 2.95f));
        for (int i = -1; i <= 1; i++)
            Box("Filter cartridge", stations[4], new Vector3(i * .25f, 1.2f, 0), new Vector3(.18f, .43f, .37f), dark, false);
        MoveStation(10, east, new Vector3(2.45f, 0, -1.55f));
        for (int i = -1; i <= 1; i++)
            Box("Specimen tray", stations[10], new Vector3(i * .43f, .94f, .34f), new Vector3(.37f, .11f, .46f), i == 0 ? ivory : dark, false);

        var dig = stations[9];
        for (int row = -1; row <= 1; row++)
        for (int col = -1; col <= 1; col++)
            Box("Excavation grid", dig, new Vector3(col * .51f, .055f, row * .51f), new Vector3(.43f, .024f, .43f),
                row == 0 && col == 0 ? orange : dark, false);
        Box("Scanner mast", dig, new Vector3(-.9f, .43f, .46f), new Vector3(.08f, .86f, .08f), ivory, false);
        Box("Scanner beacon", dig, new Vector3(-.9f, .87f, .46f), new Vector3(.21f, .15f, .17f), lamp, false);

        level.hasAnnexes = true;
        EditorSceneManager.MarkSceneDirty(scene);
        if (!EditorSceneManager.SaveScene(scene)) throw new InvalidOperationException("Could not save mission rooms.");

        void MoveStation(int index, Transform parent, Vector3 position)
        {
            stations[index].SetParent(parent, false);
            stations[index].localPosition = position;
        }
    }

    public static void ApplyPresentation()
    {
        var scene = EditorSceneManager.OpenScene(ScenePath);
        var level = UnityEngine.Object.FindFirstObjectByType<DayOneLevel>();
        var room = level.insideStart.parent;
        var dark = Material("Graphite supports");
        var blue = Material("Solar cells");
        var orange = Material("Orange equipment");
        var ivory = Material("Ivory hull");
        var glass = Material("Blue glass");
        var status = Material("Array status blue");

        foreach (var sign in level.GetComponentsInChildren<TextMesh>(true))
            UnityEngine.Object.DestroyImmediate(sign.gameObject);

        if (level.cadetBody == null)
        {
            var oldSuit = level.player.transform.Find("LunaRangers static astronaut");
            if (oldSuit != null) oldSuit.gameObject.SetActive(false);
            level.cadetBody = Marker("Cadet visual", level.player.transform, Vector3.zero);
            var body = level.cadetBody;
            SuitPart("Suit", body, new Vector3(0, .94f, 0), new Vector3(.94f, 1.05f, .67f), ivory, PrimitiveType.Capsule);
            SuitPart("Collar", body, new Vector3(0, 1.25f, .01f), new Vector3(.72f, .23f, .65f), dark);
            SuitPart("Helmet", body, new Vector3(0, 1.52f, .035f), new Vector3(.87f, .72f, .78f), ivory);
            SuitPart("Visor frame", body, new Vector3(0, 1.55f, .315f), new Vector3(.76f, .43f, .26f), dark);
            SuitPart("Visor glass", body, new Vector3(0, 1.56f, .41f), new Vector3(.66f, .34f, .13f), glass);
            SuitPart("Visor glint", body, new Vector3(-.16f, 1.63f, .467f), new Vector3(.23f, .06f, .025f), status);
            Box("Oxygen pack", body, new Vector3(0, .97f, -.39f), new Vector3(.62f, .68f, .32f), dark, false);
            SuitPart("Oxygen tank", body, new Vector3(0, 1f, -.51f), new Vector3(.4f, .55f, .32f), orange, PrimitiveType.Capsule);
            Box("Suit badge", body, new Vector3(.16f, 1.17f, .28f), new Vector3(.16f, .1f, .06f), orange, false);
            level.leftBoot = Boot("Left boot", -.24f);
            level.rightBoot = Boot("Right boot", .24f);
            level.leftArm = Arm("Left arm", -.43f);
            level.rightArm = Arm("Right arm", .43f);
        }

        if (room.Find("Habitat finish") == null)
        {
            var finish = Marker("Habitat finish", room, Vector3.zero);
            room.Find("Floor").GetComponent<MeshRenderer>().sharedMaterial = dark;
            Box("Deck inlay", finish, new Vector3(0, .008f, .25f), new Vector3(7.9f, .016f, 8.25f), blue, false);
            for (int i = -2; i <= 2; i++)
                Box("Deck seam", finish, new Vector3(0, .02f, i * 1.45f), new Vector3(7.9f, .007f, .045f), dark, false);
            foreach (float x in new[] { -3.85f, 3.85f })
            {
                Box("Safety rail", finish, new Vector3(x, .022f, .25f), new Vector3(.055f, .011f, 8.2f), ivory, false);
                for (int i = 0; i < 3; i++)
                    Box("Wall indicator", finish, new Vector3(x, 1.34f, 4.43f - i * .02f), new Vector3(.09f, .12f, .085f), status, false);
            }
            Box("Console accent", finish, new Vector3(0, 1.07f, 3.77f), new Vector3(3.7f, .045f, .035f), status, false);
            for (int i = -1; i <= 1; i++)
                Box("Airlock guide", finish, new Vector3(i * .48f, .078f, -3.72f), new Vector3(.18f, .027f, .68f), dark, false);
        }

        EditorSceneManager.MarkSceneDirty(scene);
        if (!EditorSceneManager.SaveScene(scene))
            throw new InvalidOperationException("Could not save the mission presentation.");

        Transform Boot(string name, float x)
        {
            var pivot = Marker(name, level.cadetBody, new Vector3(x, .43f, 0));
            SuitPart("Leg", pivot, new Vector3(0, -.11f, 0), new Vector3(.38f, .46f, .4f), ivory, PrimitiveType.Capsule);
            SuitPart("Boot shell", pivot, new Vector3(0, -.27f, .08f), new Vector3(.41f, .26f, .58f), dark);
            SuitPart("Toe cap", pivot, new Vector3(0, -.25f, .19f), new Vector3(.35f, .19f, .38f), ivory);
            return pivot;
        }

        Transform Arm(string name, float x)
        {
            var pivot = Marker(name, level.cadetBody, new Vector3(x, 1.15f, 0));
            SuitPart("Sleeve", pivot, new Vector3(0, -.15f, 0), new Vector3(.27f, .46f, .29f), ivory, PrimitiveType.Capsule);
            SuitPart("Glove", pivot, new Vector3(0, -.38f, .05f), new Vector3(.27f, .26f, .29f), dark);
            return pivot;
        }
    }

    private static void SuitPart(string name, Transform parent, Vector3 position, Vector3 size, Material material,
        PrimitiveType shape = PrimitiveType.Sphere)
    {
        var part = GameObject.CreatePrimitive(shape);
        part.name = name;
        part.transform.SetParent(parent, false);
        part.transform.localPosition = position;
        part.transform.localScale = size;
        part.GetComponent<MeshRenderer>().sharedMaterial = material;
        UnityEngine.Object.DestroyImmediate(part.GetComponent<Collider>());
    }

    public static void AddCampaignStations()
    {
        var scene = EditorSceneManager.OpenScene(ScenePath);
        var level = UnityEngine.Object.FindFirstObjectByType<DayOneLevel>();
        if (level.campaignStations != null && level.campaignStations.Length > 0) return;

        var room = level.insideStart.parent;
        var exterior = level.outsideStart.parent;
        var dark = Material("Graphite supports");
        var blue = Material("Solar cells");
        var orange = Material("Orange equipment");
        var ivory = Material("Ivory hull");
        var status = Material("Array status blue");
        var stations = new Transform[12];
        stations[0] = Console("Power console", new Vector3(-3.65f, 0f, -1.85f), orange, 2);
        stations[1] = level.dock;
        stations[2] = Console("Filter valve", new Vector3(3.7f, 0f, -.35f), blue, 1);
        stations[3] = level.waterStation;
        stations[4] = Console("CO2 scrubber", new Vector3(0f, 0f, 2.1f), ivory, 3);
        stations[5] = Console("Cabin monitor", new Vector3(0f, 0f, -.65f), blue, 1);
        stations[6] = Console("Crew shelter", new Vector3(-3.65f, 0f, -.15f), orange, 2);
        stations[7] = Console("Suit station", new Vector3(-2.15f, 0f, -2.8f), ivory, 2);
        stations[9] = Marker("Moon rock", exterior, level.batteryPickup.localPosition + new Vector3(-.35f, 0f, -.35f));
        Rock(stations[9], new Vector3(0f, .20f, 0f), .45f);
        Box("Sample marker", stations[9], new Vector3(0f, .025f, 0f), new Vector3(.9f, .035f, .85f), orange, false);
        stations[10] = Console("Sample locker", new Vector3(3.65f, 0f, 2.75f), orange, 2);
        stations[11] = Console("Mission terminal", new Vector3(-2.45f, 0f, 2.95f), blue, 1);
        level.campaignStations = stations;
        level.carriedSample = Rock(level.player.transform, new Vector3(.44f, .9f, .16f), .28f);
        level.storedSample = Rock(stations[10], new Vector3(0f, 1.12f, 0f), .34f);
        level.solarStatus = Box("Array online", stations[0], new Vector3(.21f, 1.07f, -.22f),
            new Vector3(.14f, .06f, .14f), status, false);

        stations[9].gameObject.SetActive(false);
        level.carriedSample.SetActive(false);
        level.storedSample.SetActive(false);
        level.solarStatus.SetActive(false);
        EditorSceneManager.MarkSceneDirty(scene);
        if (!EditorSceneManager.SaveScene(scene))
            throw new InvalidOperationException("Could not save campaign equipment.");

        Transform Console(string title, Vector3 position, Material surface, int vents)
        {
            var station = Marker(title, room, position);
            Box("Housing", station, new Vector3(0f, .48f, 0f), new Vector3(.82f, .96f, .7f), surface, false);
            Box("Control surface", station, new Vector3(0f, .98f, 0f), new Vector3(.72f, .12f, .52f), dark, false);
            for (int i = 0; i < vents; i++)
                Box("Control light", station, new Vector3((i - (vents - 1) * .5f) * .17f, 1.065f, .02f),
                    new Vector3(.10f, .06f, .13f), status, false);
            return station;
        }

        GameObject Rock(Transform parent, Vector3 position, float scale)
        {
            var rock = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            rock.name = "Rock sample";
            rock.transform.SetParent(parent, false);
            rock.transform.localPosition = position;
            rock.transform.localScale = new Vector3(scale, scale * .65f, scale * .84f);
            rock.GetComponent<MeshRenderer>().sharedMaterial = dark;
            UnityEngine.Object.DestroyImmediate(rock.GetComponent<SphereCollider>());
            rock.transform.localRotation = Quaternion.Euler(22f, 37f, 16f);
            return rock;
        }
    }

    public static void PolishExistingScene()
    {
        var scene = EditorSceneManager.OpenScene(ScenePath);
        var level = UnityEngine.Object.FindFirstObjectByType<DayOneLevel>();
        if (level.transform.Find("Exterior ground") == null)
        {
            var ground = Marker("Exterior ground", level.transform, new Vector3(-4.325f, -.12f, -3.575f));
            ground.gameObject.AddComponent<BoxCollider>().size = new Vector3(8f, .24f, 6f);
        }

        var room = level.insideStart.parent;
        if (room.Find("Habitat details") == null)
        {
            var details = Marker("Habitat details", room, Vector3.zero);
            var dark = Material("Graphite supports");
            var blue = Material("Solar cells");
            var ivory = Material("Ivory hull");
            for (int i = 0; i < 3; i++)
            {
                float x = (i - 1) * 2.9f;
                Box("Wall bay", details, new Vector3(x, 1.75f, 4.62f), new Vector3(2.55f, 2.4f, .12f), dark, false);
                Box("Inset panel", details, new Vector3(x, 1.82f, 4.54f), new Vector3(2.3f, 1.9f, .08f), blue, false);
                Box("Bay trim", details, new Vector3(x, 2.91f, 4.47f), new Vector3(2.3f, .10f, .08f), ivory, false);
            }
            foreach (float x in new[] { -4.35f, 4.35f })
            {
                Box("Floor rail", details, new Vector3(x, .013f, 0), new Vector3(.18f, .022f, 8.4f), dark, false);
                for (int i = 0; i < 6; i++)
                    Box("Route marker", details, new Vector3(x, .028f, i * 1.25f - 3.2f), new Vector3(.14f, .018f, .34f), ivory, false);
            }
        }
        if (level.heaterLight.GetComponentInChildren<Light>(true) == null)
        {
            var glow = Marker("Heater glow", level.heaterLight.transform, Vector3.zero);
            glow.position = level.heater.position + new Vector3(0f, 1.1f, -.85f);
            var light = glow.gameObject.AddComponent<Light>();
            light.type = LightType.Point;
            light.color = new Color(1f, .62f, .26f);
            light.range = 4.4f;
            light.intensity = 0f;
        }

        EditorSceneManager.MarkSceneDirty(scene);
        if (!EditorSceneManager.SaveScene(scene))
            throw new InvalidOperationException("Could not save Day 1 visual updates.");
    }

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
        {
            Create();
            PolishExistingScene();
            AddCampaignStations();
            ApplyPresentation();
            ApplyMissionRooms();
        }

        string[] args = Environment.GetCommandLineArgs();
        int outputArg = Array.IndexOf(args, "-dayOneOutput");
        if (outputArg < 0) return;
        string output = args[outputArg + 1];
        Directory.CreateDirectory(Path.GetDirectoryName(output));
        var target = EditorUserBuildSettings.activeBuildTarget == BuildTarget.WebGL
            ? BuildTarget.WebGL : BuildTarget.StandaloneWindows64;
        string originalTemplate = PlayerSettings.WebGL.template;
        BuildReport report;
        try
        {
            if (target == BuildTarget.WebGL) PlayerSettings.WebGL.template = "PROJECT:LunaRangers";
            report = BuildPipeline.BuildPlayer(new BuildPlayerOptions
            {
                scenes = new[] { ScenePath },
                target = target,
                locationPathName = output,
                options = BuildOptions.None
            });
        }
        finally
        {
            if (target == BuildTarget.WebGL) PlayerSettings.WebGL.template = originalTemplate;
        }
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
        level.outsideView = View("Outside camera", exterior, new Vector3(5, 8.5f, -13), new Vector3(-2.9f, .75f, -2.7f));

        var room = Marker("Habitat interior", parent, new Vector3(80, 0, 0));
        Box("Floor", room, new Vector3(0, -.13f, 0), new Vector3(10, .26f, 10), trim);
        Box("Rear bulkhead", room, new Vector3(0, 1.65f, 4.8f), new Vector3(10, 3.3f, .3f), ivory);
        foreach (float x in new[] { -4.9f, 4.9f })
            Box("Side bulkhead", room, new Vector3(x, 1.2f, .4f), new Vector3(.3f, 2.4f, 8.8f), ivory);
        Box("Console shelf", room, new Vector3(0, 1.02f, 4.2f), new Vector3(4.2f, .16f, .8f), dark);
        Box("Airlock threshold", room, new Vector3(0, .025f, -3.7f), new Vector3(2.1f, .05f, 1f), orange, false);
        level.insideAirlock = Marker("Inside hatch", room, new Vector3(0, 0, -3.55f));
        level.insideStart = Marker("Inside spawn", room, new Vector3(0, .03f, -2.45f));
        level.insideView = View("Inside camera", room, new Vector3(0, 10.5f, -11.5f), new Vector3(0, .4f, .3f));

        level.dock = Marker("Battery dock", room, new Vector3(2.9f, 0, 1.25f));
        Box("Dock base", level.dock, new Vector3(0, .27f, 0), new Vector3(1.3f, .54f, 1.1f), dark);
        Box("Dock guide", level.dock, new Vector3(0, .57f, 0), new Vector3(1.07f, .08f, .85f), orange);
        level.dockedBattery = Battery("Docked battery", level.dock, new Vector3(0, .94f, 0), orange, dark);

        level.heater = Marker("Heater", room, new Vector3(-2.9f, 0, 1.25f));
        Box("Heater case", level.heater, new Vector3(0, .84f, 0), new Vector3(1.56f, 1.68f, .87f), orange);
        Box("Heater front", level.heater, new Vector3(0, .84f, -.45f), new Vector3(1.29f, 1.35f, .08f), ivory, false);
        for (int i = 0; i < 3; i++)
            Box("Heater grille", level.heater, new Vector3(0, .83f + i * .13f, -.504f), new Vector3(.93f, .055f, .04f), dark, false);
        level.heaterLight = Box("Heat indicator", level.heater, new Vector3(0, 1.35f, -.5f), new Vector3(.35f, .12f, .06f), Material("Array status blue"), false);
        Box("Power conduit", room, new Vector3(0, .04f, 1.28f), new Vector3(5.2f, .08f, .13f), orange, false);

        level.waterStation = Marker("Water station", room, new Vector3(3.78f, 0, -2.18f));
        Box("Water station base", level.waterStation, new Vector3(0, .46f, 0), new Vector3(.85f, .92f, .7f), blue);
        Box("Water cartridge", level.waterStation, new Vector3(0, 1.18f, 0), new Vector3(.57f, .53f, .48f), trim);
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
        Require(day.TryConnect(1, 1) && !day.HeaterOn && day.TryConnect(2, 2) && day.HeaterOn,
            "All three matches restore heat.");
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
