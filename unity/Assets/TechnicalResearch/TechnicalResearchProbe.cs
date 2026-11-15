using System;
using System.Runtime.InteropServices;
using UnityEngine;

// Throwaway feasibility probe: no mission rules or scientific resource values.
public sealed class TechnicalResearchProbe : MonoBehaviour
{
    public Renderer panelRenderer;
    private Material panelMaterial;
    private bool panelEnabled = true;
    private int revision;

    [Serializable]
    private sealed class Snapshot
    {
        public string type;
        public bool panelEnabled;
        public int revision;
        public int frame;
        public string error;
    }

#if UNITY_WEBGL && !UNITY_EDITOR
    [DllImport("__Internal")] private static extern void PublishResearchState(string json);
#endif

    private void Start()
    {
        if (!panelRenderer) { Debug.LogError("Probe panel renderer is missing."); enabled = false; return; }
        panelMaterial = panelRenderer.material;
        Publish("ready");
    }

    public void ReceiveCommand(string command)
    {
        if (command != "toggle") { Publish("rejected", "unknown-command"); return; }
        if (!panelMaterial) { Publish("rejected", "not-ready"); return; }
        panelEnabled = !panelEnabled;
        revision++;
        panelMaterial.SetColor("_BaseColor", panelEnabled ? new Color(0.08f, 0.35f, 0.7f) : new Color(0.8f, 0.3f, 0.05f));
        Publish("state");
    }

    private void Publish(string type, string error = "")
    {
        var json = JsonUtility.ToJson(new Snapshot { type = type, panelEnabled = panelEnabled, revision = revision, frame = Time.frameCount, error = error });
#if UNITY_WEBGL && !UNITY_EDITOR
        PublishResearchState(json);
#else
        Debug.Log("ResearchProbe: " + json);
#endif
    }

    private void OnDestroy() { if (panelMaterial) Destroy(panelMaterial); }
}
