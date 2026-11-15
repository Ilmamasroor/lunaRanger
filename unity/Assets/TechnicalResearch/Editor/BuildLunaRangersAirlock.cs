using System;
using System.Collections.Generic;
using System.Linq;
using UnityEditor;
using UnityEditor.Build;
using UnityEditor.Build.Reporting;
using UnityEngine;
using UnityEngine.SceneManagement;

public sealed class BuildLunaRangersAirlock : IProcessSceneWithReport
{
    private const string ScenePath = "Assets/TechnicalResearch/LunaRangersOutpost.unity";
    private static bool buildingDemo;

    public int callbackOrder => 0;

    public static void Build()
    {
        string[] args = Environment.GetCommandLineArgs();
        string output = args[Array.IndexOf(args, "-airlockOutput") + 1];
        var originalCompression = PlayerSettings.WebGL.compressionFormat;
        try
        {
            buildingDemo = true;
            PlayerSettings.WebGL.compressionFormat = WebGLCompressionFormat.Brotli;
            var report = BuildPipeline.BuildPlayer(new BuildPlayerOptions
            {
                scenes = new[] { ScenePath },
                locationPathName = output,
                target = BuildTarget.WebGL,
                options = BuildOptions.None
            });
            if (report.summary.result != BuildResult.Succeeded)
                throw new BuildFailedException("Airlock build failed: " + report.summary.result);

            Debug.Log($"Airlock demo built: {report.summary.totalSize} bytes");
        }
        finally
        {
            PlayerSettings.WebGL.compressionFormat = originalCompression;
            buildingDemo = false;
        }
    }

    public void OnProcessScene(Scene scene, BuildReport report)
    {
        if (!buildingDemo || scene.path != ScenePath)
            return;

        var roots = scene.GetRootGameObjects();
        var airlock = new GameObject("AirlockDemo").AddComponent<LunaRangersAirlock>();
        SceneManager.MoveGameObjectToScene(airlock.gameObject, scene);
        airlock.sceneCamera = roots.Single(root => root.CompareTag("MainCamera")).GetComponent<Camera>();
        airlock.transform.position = new Vector3(-3.4f, 1.65f, -.62f);
        airlock.clickTarget = airlock.gameObject.AddComponent<BoxCollider>();
        airlock.clickTarget.size = new Vector3(1.65f, 2.15f, .5f);
        airlock.door = new GameObject("Sliding hatch").transform;
        airlock.door.SetParent(airlock.transform, false);

        var filters = roots.SelectMany(root => root.GetComponentsInChildren<MeshFilter>()).ToArray();
        MoveBakedPart(filters, "Structural ribs", "Hatch", new Vector3(-3.4f, 1.65f, -.62f), new Vector3(1.27f, 1.8f, .09f), airlock.door);
        var dark = MoveBakedPart(filters, "Blue glass", "Hatch window", new Vector3(-3.4f, 1.85f, -.68f), new Vector3(.8f, .65f, .045f), airlock.door);
        MoveBakedPart(filters, "Graphite supports", "Handle", new Vector3(-2.92f, 1.32f, -.70f), new Vector3(.08f, .35f, .06f), airlock.door);
        AddBox("Airlock interior", new Vector3(-3.4f, 1.65f, -.604f), new Vector3(1.25f, 1.78f, .014f), dark, airlock.transform);
    }

    private static Material MoveBakedPart(MeshFilter[] filters, string materialName, string partName, Vector3 center, Vector3 size, Transform parent)
    {
        var filter = filters.Single(item => item.name == "Batched " + materialName);
        var mesh = UnityEngine.Object.Instantiate(filter.sharedMesh);
        var bounds = new Bounds(center, size + Vector3.one * .002f);
        var vertices = mesh.vertices;
        var triangles = mesh.triangles;
        var remaining = new List<int>(triangles.Length);
        for (int i = 0; i < triangles.Length; i += 3)
        {
            if (bounds.Contains(vertices[triangles[i]]) && bounds.Contains(vertices[triangles[i + 1]]) && bounds.Contains(vertices[triangles[i + 2]]))
                continue;

            remaining.Add(triangles[i]);
            remaining.Add(triangles[i + 1]);
            remaining.Add(triangles[i + 2]);
        }

        if (triangles.Length - remaining.Count != 36)
            throw new BuildFailedException($"Could not isolate the 12 triangles for {partName}.");

        mesh.SetTriangles(remaining, 0);
        filter.sharedMesh = mesh;
        var material = filter.GetComponent<MeshRenderer>().sharedMaterial;
        AddBox(partName, center, size, material, parent);
        return material;
    }

    private static void AddBox(string name, Vector3 position, Vector3 size, Material material, Transform parent)
    {
        var part = GameObject.CreatePrimitive(PrimitiveType.Cube);
        UnityEngine.Object.DestroyImmediate(part.GetComponent<Collider>());
        part.name = name;
        part.transform.SetParent(parent, false);
        part.transform.position = position;
        part.transform.localScale = size;
        part.GetComponent<MeshRenderer>().sharedMaterial = material;
    }
}
