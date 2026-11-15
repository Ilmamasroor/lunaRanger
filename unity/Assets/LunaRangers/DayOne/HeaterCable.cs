using UnityEngine;

namespace LunaRangers.DayOne
{
    public sealed class HeaterCable : UnityEngine.UI.Graphic
    {
        private Vector2 start, end;

        public void SetEnds(Vector2 from, Vector2 to)
        {
            if (from == start && to == end) return;
            start = from;
            end = to;
            SetVerticesDirty();
        }

        protected override void OnPopulateMesh(UnityEngine.UI.VertexHelper mesh)
        {
            mesh.Clear();
            const int segments = 24;
            var tangent = Vector2.right * Mathf.Min(90f, Mathf.Abs(end.x - start.x) * .45f);
            var previous = start;
            for (int i = 0; i <= segments; i++)
            {
                float t = i / (float)segments;
                float u = 1f - t;
                Vector2 point = u * u * u * start + 3f * u * u * t * (start + tangent)
                    + 3f * u * t * t * (end - tangent) + t * t * t * end;
                Vector2 direction = i == 0 ? Vector2.right : (point - previous).normalized;
                Vector2 normal = new Vector2(-direction.y, direction.x) * 4f;
                mesh.AddVert(point + normal, color, Vector2.zero);
                mesh.AddVert(point - normal, color, Vector2.zero);
                if (i > 0)
                {
                    int index = i * 2;
                    mesh.AddTriangle(index - 2, index, index - 1);
                    mesh.AddTriangle(index - 1, index, index + 1);
                }
                previous = point;
            }
        }
    }
}
