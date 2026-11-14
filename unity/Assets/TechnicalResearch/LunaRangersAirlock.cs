using System.Runtime.InteropServices;
using UnityEngine;
using UnityEngine.InputSystem;

public sealed class LunaRangersAirlock : MonoBehaviour
{
    public Camera sceneCamera;
    public BoxCollider clickTarget;
    public Transform door;

    private Vector3 closedPosition;

#if UNITY_WEBGL && !UNITY_EDITOR
    [DllImport("__Internal")]
    private static extern void PublishAirlockEvent(string type);
#endif

    private void Awake() => closedPosition = door.localPosition;

    private void Update()
    {
        var mouse = Mouse.current;
        if (mouse == null || !mouse.leftButton.wasPressedThisFrame)
            return;

        Ray ray = sceneCamera.ScreenPointToRay(mouse.position.ReadValue());
        if (clickTarget.Raycast(ray, out _, sceneCamera.farClipPlane))
            Publish("selected");
    }

    public void ApplyAirlockState(string state)
    {
        switch (state)
        {
            case "approved":
                door.localPosition = closedPosition + Vector3.up * 1.85f;
                Publish("opened");
                break;
            case "reset":
                door.localPosition = closedPosition;
                Publish("closed");
                break;
        }
    }

    private static void Publish(string type)
    {
#if UNITY_WEBGL && !UNITY_EDITOR
        PublishAirlockEvent(type);
#else
        Debug.Log("Airlock: " + type);
#endif
    }
}
