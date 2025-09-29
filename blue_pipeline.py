import os
import json
import re
from gpt_interface import GPT4Bot

TAGHELPER_CODE = '''using UnityEditor;
using UnityEngine;
using System.Reflection;

public static class TagHelper
{
    public static void AddTagIfNotExists(string tag)
    {
        SerializedObject tagManager = new SerializedObject(AssetDatabase.LoadAllAssetsAtPath("ProjectSettings/TagManager.asset")[0]);
        SerializedProperty tagsProp = tagManager.FindProperty("tags");
        bool found = false;
        for (int i = 0; i < tagsProp.arraySize; i++)
        {
            SerializedProperty t = tagsProp.GetArrayElementAtIndex(i);
            if (t.stringValue.Equals(tag)) { found = true; break; }
        }
        if (!found)
        {
            tagsProp.InsertArrayElementAtIndex(0);
            SerializedProperty n = tagsProp.GetArrayElementAtIndex(0);
            n.stringValue = tag;
            tagManager.ApplyModifiedProperties();
        }
    }
}
'''
taghelper_path = "UnityProject/Assets/Editor/TagHelper.cs"
with open(taghelper_path, "w", encoding="utf-8") as f:
    f.write(TAGHELPER_CODE)
    print(f"TagHelper.cs saved.")


# Write UIHelper.cs
UIHELPER_CODE = '''using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

public static class UIHelper
{
    // Automatically generate a Text object under the Canvas with a centered font, size, and anchor.
    public static GameObject CreateText(string name, string text, Transform parent, int fontSize = 64, Color? color = null)
    {
        GameObject go = new GameObject(name);
        go.transform.SetParent(parent, false);
        var textComp = go.AddComponent<Text>();
        textComp.text = text;
        textComp.font = Resources.GetBuiltinResource<Font>("Arial.ttf");
        textComp.fontSize = fontSize;
        textComp.alignment = TextAnchor.MiddleCenter;
        textComp.color = color ?? Color.white;
        var rect = go.GetComponent<RectTransform>();
        rect.sizeDelta = new Vector2(800, 240);
        rect.anchorMin = Vector2.zero;
        rect.anchorMax = Vector2.one;
        rect.offsetMin = Vector2.zero;
        rect.offsetMax = Vector2.zero;
        go.SetActive(false); // Hidden by default
        return go;
    }
}
'''
uihelper_path = "UnityProject/Assets/Editor/UIHelper.cs"
with open(uihelper_path, "w", encoding="utf-8") as f:
    f.write(UIHELPER_CODE)
    print(f"UIHelper.cs saved.")

# Create UIManager.cs
UIMANAGER_CS = '''using UnityEngine;
public class UIManager : MonoBehaviour
{
    public GameObject winText;
    public GameObject failText;
    void Awake()
    {
        if (winText == null) winText = GameObject.Find("WinText");
        if (failText == null) failText = GameObject.Find("FailText");
        if (winText != null) winText.SetActive(false);
        if (failText != null) failText.SetActive(false);
    }
    public void ShowWin()
    {
        if (winText != null) winText.SetActive(true);
        if (failText != null) failText.SetActive(false);
    }
    public void ShowFail()
    {
        if (failText != null) failText.SetActive(true);
        if (winText != null) winText.SetActive(false);
    }
    public void HideAllUI()
    {
        if (winText != null) winText.SetActive(false);
        if (failText != null) failText.SetActive(false);
    }
}
'''
uimanager_path = "UnityProject/Assets/Scripts/UIManager.cs"
with open(uimanager_path, "w", encoding="utf-8") as f:
    f.write(UIMANAGER_CS)
    print(f"UIManager.cs saved.")

# Create UIManagerAutoCreator.cs
UI_MANAGER_AUTO_CREATOR_CS = '''using UnityEditor;
using UnityEngine;
using UnityEngine.UI;

public static class UIManagerAutoCreator
{
    public static void CreateUIManagerGO()
    {
        // Create Canvas (if it doesn't exist)
        GameObject canvasGO = GameObject.Find("Canvas");
        if (canvasGO == null)
        {
            // Create a new Canvas
            GameObject canvasObject = new GameObject("Canvas");
            Canvas canvas = canvasObject.AddComponent<Canvas>();
            canvas.renderMode = RenderMode.ScreenSpaceOverlay;  // Set to Screen Space
            canvasObject.AddComponent<CanvasScaler>();  // Add CanvasScaler component
            canvasObject.AddComponent<GraphicRaycaster>();  // Add GraphicRaycaster component
            canvasGO = canvasObject;
        }

        // Use TagHelper to add the tag for Canvas
        TagHelper.AddTagIfNotExists("Canvas");

        // Create WinText (if it doesn't exist)
        CreateTextGO("WinText", "Game Win", canvasGO.transform);

        // Use TagHelper to add the tag for WinText
        TagHelper.AddTagIfNotExists("WinText");

        // Create FailText (if it doesn't exist)
        CreateTextGO("FailText", "Game Over", canvasGO.transform);

        // Use TagHelper to add the tag for FailText
        TagHelper.AddTagIfNotExists("FailText");

        // Create UIManager (if it doesn't exist)
        GameObject uiManagerGO = GameObject.Find("UIManager");
        if (uiManagerGO == null)
        {
            uiManagerGO = new GameObject("UIManager");
            uiManagerGO.AddComponent<UIManager>();  // Add UIManager script
            uiManagerGO.tag = "UIManager";  // Add UIManager tag
            uiManagerGO.layer = LayerMask.NameToLayer("UI");
            Selection.activeGameObject = uiManagerGO;  // Select the created UIManager
        }

        // Set WinText and FailText for the UIManager component
        UIManager uiManagerScript = uiManagerGO.GetComponent<UIManager>();
        if (uiManagerScript != null)
        {
            GameObject winTextGO = GameObject.Find("WinText");
            GameObject failTextGO = GameObject.Find("FailText");

            // Drag WinText and FailText to the UIManager script fields
            if (winTextGO != null)
            {
                uiManagerScript.winText = winTextGO;
                winTextGO.SetActive(true);  // Ensure WinText is visible when created
            }
            if (failTextGO != null)
            {
                uiManagerScript.failText = failTextGO;
                failTextGO.SetActive(true);  // Ensure FailText is visible when created
            }
        }

        // Set Canvas tag
        canvasGO.tag = "Canvas";
        canvasGO.layer = LayerMask.NameToLayer("UI");

        // Select the generated Canvas
        Selection.activeGameObject = canvasGO;
    }

    private static void CreateTextGO(string textName, string displayText, Transform parent)
    {
        GameObject textGO = GameObject.Find(textName);
        if (textGO == null)
        {
            textGO = UIHelper.CreateText(textName, displayText, parent);
            textGO.tag = textName;
            textGO.layer = LayerMask.NameToLayer("UI");
            textGO.SetActive(true);  // Ensure text is visible when created
        }
        else
        {
            // If text already exists, select it
            Selection.activeGameObject = textGO;
        }
    }
}
'''
ui_manager_auto_creator_path = "UnityProject/Assets/Editor/UIManagerAutoCreator.cs"
with open(ui_manager_auto_creator_path, "w", encoding="utf-8") as f:
    f.write(UI_MANAGER_AUTO_CREATOR_CS)
    print(f"UIManagerAutoCreator.cs saved.")

# Create ReflectionHelper.cs
REFLECTION_HELPER_CODE = """using UnityEngine;
using UnityEditor;
using System;
using System.Reflection;

public static class ReflectionHelper
{
    // A more robust method for setting fields of any type
    public static void SetValue(object obj, string fieldName, object value)
    {
        if (obj == null)
        {
            Debug.LogError("ReflectionHelper: Target object is null.");
            return;
        }

        Type t = obj.GetType();
        FieldInfo field = t.GetField(fieldName, BindingFlags.Instance | BindingFlags.Public | BindingFlags.NonPublic);

        if (field == null)
        {
            // The field was not found, which is a common occurrence.
            // We can log a warning instead of an error here.
            return;
        }

        // Handle Unity Object references separately
        if (value is UnityEngine.Object && field.FieldType.IsSubclassOf(typeof(UnityEngine.Object)) || field.FieldType == typeof(UnityEngine.Object))
        {
            if (field.FieldType.IsInstanceOfType(value))
            {
                field.SetValue(obj, value);
            }
            else
            {
                Debug.LogError($"ReflectionHelper: Failed to assign object to field '{fieldName}'. Type mismatch. Found: {value.GetType().Name}, Expected: {field.FieldType.Name}");
            }
        }
        else
        {
            // Handle primitive types and strings
            try
            {
                object convertedValue = Convert.ChangeType(value, field.FieldType);
                field.SetValue(obj, convertedValue);
            }
            catch (Exception e)
            {
                Debug.LogError($"ReflectionHelper: Failed to convert and set field '{fieldName}'. Error: {e.Message}");
            }
        }
    }
}
"""
reflection_helper_path = "UnityProject/Assets/Editor/ReflectionHelper.cs"
with open(reflection_helper_path, "w", encoding="utf-8") as f:
    f.write(REFLECTION_HELPER_CODE)
    print(f"ReflectionHelper.cs saved.")

def legalize_name(name):
    """Replaces illegal characters in C# variable/Unity GameObject names with underscores."""
    if not isinstance(name, str):
        name = str(name)
    return re.sub(r'[^0-9a-zA-Z_]', '_', name)

FIELD_TYPE_MAP = {
    "GameObject": "GameObject",
    "Transform": "Transform",
    "Animator": "Animator",
    "AudioSource": "AudioSource",
    "AnimationClip": "AnimationClip",
    "float": "float",
    "int": "int",
    "string": "string"
}

def generate_field_code(fields: dict):
    lines = []
    for field, ref in fields.items():
        if isinstance(ref, dict):
            ftype = FIELD_TYPE_MAP.get(ref.get("type", "GameObject"), "GameObject")
        else:
            ftype = "GameObject"
        # Default float with initial value
        if ftype == "float":
            lines.append(f"    public float {field} = 0f;")
        elif ftype == "int":
            lines.append(f"    public int {field} = 0;")
        elif ftype == "string":
            lines.append(f"    public string {field} = \"\";")
        else:
            lines.append(f"    public {ftype} {field};")
    return "\n".join(lines)

def get_required_usings(blueprint):
    usings = set(["using UnityEngine;", "using UnityEditor;"])
    ui_types = {"Image", "GraphicRaycaster", "CanvasScaler"}
    event_types = {"EventSystem", "StandaloneInputModule"}
    # Check components field
    if any(c in ui_types for c in blueprint.get("components", [])):
        usings.add("using UnityEngine.UI;")
    if any(c in event_types for c in blueprint.get("components", [])):
        usings.add("using UnityEngine.EventSystems;")
    return "\n".join(sorted(usings))

class BlueprintGenerator:
    def __init__(self, bot):
        self.bot = bot

    def generate_blueprints(self, asset_info, game_description):
        # Upgraded prompt, script_fields explicitly specify type (Transform/GameObject/Animator/...)
        prompt = (
            "You are a Unity game architecture expert. Based on the following description, generate a JSON array of GameObject blueprints. Each object must include:\n"
            "- name (must be unique)\n"
            "- create_type (module/primitive/empty)\n"
            "- asset_path\n"
            "- primitive_type\n"
            "- position\n"
            "- rotation\n"
            "- scale\n"
            "- tag (e.g., MainCamera, must correspond to name)\n"
            "- layer\n"
            "- components (e.g., Character Controller)\n"
            "- scripts\n"
            "- script_fields\n"
            "【Unique Naming Convention】\n"
            "- All key GameObjects (e.g., player ball, camera, endpoint) must have a unique name. The name cannot be the default “Cube”, “Sphere”, but should be like “Player”, “MainCamera”, “EndPoint”, etc., and the tag should correspond to the name (e.g., Player).\n"
            "- Any GameObject that needs to be referenced by a script (e.g., CameraFollow.target) must have a unique name and is recommended to have a tag.\n"
            "【Components Logic】\n"
            "- For any objects that need to be affected by physics (e.g., gravity, forces) or **to correctly collide with other physics-based objects**, a 'Rigidbody' component must be included.\n"
            "- For player characters that need precise, non-physics-based movement (e.g., walking, jumping in a platformer), a 'CharacterController' component must be included. A CharacterController is not affected by forces and will only move when you call its Move function.\n"
            "【WinText/FailText Special Rules】\n"
            "- WinText and FailText do not need to be automatically generated in the blueprint.\n"
            "- The actual display content of WinText and FailText is automatically generated by UIHelper.CreateText, with content being “Game Win” and “Game Over” respectively.\n"
            "【UIManager Special Rules】\n"
            "- UIManager does not need to be automatically generated in the blueprint.\n"
            "- The script_fields for UIManager should only be written like this: {'UIManager': {'winText': {'go':'WinText'}, 'failText': {'go':'FailText'}}}\n"
            "- The UIManager script needs to implement the ShowWin/ShowFail/HideAllUI methods to control the display/hide of WinText and FailText respectively.\n"
            "【script_fields Field Pointers】\n"
            "- When the script_fields field references a target GameObject, you must strictly write the unique name of the target object.\n"
            "- Example: If the CameraFollow.target of the main camera should point to the player ball, the player ball's name must be “Player”, and the target's go in script_fields should be written as “Player”, with type as “Transform”.\n"
            "【Vector3/Vector Type Fields】\n"
            "- Vector3 type fields like offset, position, rotation, and scale must be filled directly as a triplet array, such as [0,2.0,-3.5], and must not be written as a {'go':...,'type':...} structure or left empty. They must be valid numeric triplets."
            "- Only GameObject/Transform/references, etc., are allowed to use the go/type structure.\n"
            "The format is like {'script name': {'field name': {'go': 'target GO name', 'type': 'Transform/Animator/AudioSource/GameObject/other type'}}}),"
            "for example, if CameraFollow.target points to Player's Transform, it should be written as:"
            "{'script_fields':{'CameraFollow': {'target': {'go':'Player','type':'Transform'}}}}\n"
            "If asset_path cannot be found, set create_type to primitive or empty.\n"
            f"🎮 Game Description: {game_description}\n"
            f"📦 Asset Information: {json.dumps(asset_info, indent=2, ensure_ascii=False)}\n"
            "Please strictly output a Markdown code block JSON array (no comments, no explanations)."
        )
        response = self.bot.ask(prompt)
        code = response
        if code.startswith("```"):
            # Remove markdown code block ```
            code = "\n".join(line for line in code.splitlines() if not line.strip().startswith("```"))
        blueprints = json.loads(code)
        for bp in blueprints:
            bp["name"] = legalize_name(bp["name"])
            if "script_fields" not in bp:
                bp["script_fields"] = {}
        return blueprints


class DescriptionGenerator:
    def __init__(self, bot):
        self.bot = bot

    def generate_script_descriptions(self, game_description, scripts_to_describe):
        script_list_str = ", ".join(scripts_to_describe)

        prompt = (
            f"You are a Unity game development expert. Based on the following game description, generate a detailed C# function description for each script needed. "
            f"Focus on step-by-step logic and the specific Unity APIs to use. "
            f"The scripts to describe are: {script_list_str}. "
            f"Each description should be a detailed, multi-step algorithm that an experienced C# programmer can follow to implement the game logic. "
            f"For example, for player movement, specify using `FixedUpdate` and `Rigidbody.MovePosition`. "
            f"For AI, specify using `Vector3.MoveTowards`, `Physics.OverlapSphere`, etc. "
            f"Output a JSON object where the key is the script name and the value is the detailed description. "
            f"Do not include any extra text, explanations, or markdown outside of the JSON object.\n\n"
            f"Game Description:\n{game_description}"
        )

        response = self.bot.ask(prompt)

        # Clean the response to ensure it's a valid JSON object
        response = re.sub(r"```json|```", "", response).strip()
        try:
            return json.loads(response)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from DescriptionGenerator: {e}")
            print(f"Raw response:\n{response}")
            return {}


class CSharpScriptGenerator:
    def __init__(self, bot):
        self.bot = bot

    def generate_script(self, go_name, script_name, description, script_fields, all_script_names):
        fields_code = generate_field_code(script_fields)

        # New: Create a prompt part with all script names
        all_scripts_prompt = "【All Scripts in the Project】:\n" + ", ".join(all_script_names)

        prompt_parts = [
            f"You are a senior Unity C# development expert. Please generate the script '{script_name}.cs' for the GameObject '{go_name}'.",
            f"【Function Description】:\n{description}\n",
            f"【Field Definitions】(all public):\n{fields_code}\n",
            all_scripts_prompt,
            "Note: Please prioritize using the CharacterController's built-in collision detection for triggers.",
            "Note: Assume no manually set will be made, e.g. GhostPatrol can automatically create patrol points for itself."
            "//【Reference Code Snippets】:",
            "// UIManager and Win/Fail logic",
            "// IMPORTANT: Do NOT use GameManager. Only use UIManager for win/fail UI control.",
            "// UIManager.cs already exists and has:",
            "//     public void ShowWin()",
            "//     public void ShowFail()",
            "public UIManager uiManager;",
            "void FindUIManager() { uiManager = FindObjectOfType<UIManager>(); }",
            "void ShowWin() { if (uiManager != null) uiManager.ShowWin(); }",
            "void ShowFail() { if (uiManager != null) uiManager.ShowFail(); }",
            "",
            "// CameraFollow logic",
            "// This script should be named CameraFollow.cs and implement the following logic.",
            "public Transform target;",
            "public Vector3 offset = new Vector3(0f, 2.0f, -3.5f);",
            "public float smoothSpeed = 5f;",
            "void LateUpdate() {",
            "    if (target == null) return;",
            "    Vector3 desiredPosition = target.position + offset;",
            "    Vector3 smoothedPosition = Vector3.Lerp(transform.position, desiredPosition, smoothSpeed * Time.deltaTime);",
            "    transform.position = smoothedPosition;",
            "    transform.LookAt(target);",
            "}",
            "",
            "// Player Movement Logic (CharacterController)",
            "// Use this code to implement movement based on input.",
            "public float turnSpeed = 120f;",
            "public float moveSpeed = 5f;",
            "private CharacterController m_CharacterController;",
            "private Animator m_Animator;",
            "void Awake()",
            "{",
            "    m_CharacterController = GetComponent<CharacterController>();",
            "    m_Animator = GetComponent<Animator>();",
            "}",
            "void Update()",
            "{",
            "    float horizontal = Input.GetAxis(\"Horizontal\");",
            "    float vertical = Input.GetAxis(\"Vertical\");",
            "    Vector3 moveDirection = new Vector3(horizontal, 0f, vertical).normalized;",
            "    if (moveDirection.magnitude >= 0.1f)",
            "    {",
            "        float targetAngle = Mathf.Atan2(moveDirection.x, moveDirection.z) * Mathf.Rad2Deg;",
            "        Quaternion newRotation = Quaternion.Euler(0, targetAngle, 0);",
            "        transform.rotation = Quaternion.Slerp(transform.rotation, newRotation, turnSpeed * Time.deltaTime);",
            "        m_CharacterController.Move(moveDirection * moveSpeed * Time.deltaTime);",
            "    }",
            "    if (m_Animator != null)",
            "    {",
            "        bool isMoving = moveDirection.magnitude > 0.1f;",
            "        m_Animator.SetBool(\"IsWalking\", isMoving);",
            "    }",
            "}"
            "// --- Patrol / AI Movement Logic ---",
            "// Patrol must work even if no manual waypoints are set.",
            "// Support patrol modes: Square, Line, Random (with points generated within a radius).",
            "// Use ping-pong logic (back and forth) instead of looping.",
            "// Waypoints should be generated automatically in Start if none exist.",
            "// Rigidbody.MovePosition should be used inside FixedUpdate to move smoothly.",
            "// Transform.forward should be aligned with movement direction."
        ]

        prompt = "\n".join(prompt_parts)
        prompt += "\n\n【Output Requirements】:\n- Only output the complete C# script file content, including all using statements, the complete class definition, and all fields and methods.\n- Do not output a Markdown code block, comments, or any extra text. Just the C# code."

        code = self.bot.ask(prompt)
        # Force keep only C# code, remove Markdown code blocks
        code = re.sub(r"```[^\n]*\n?", "", code).strip()
        # Add missing brackets if needed
        left = code.count("{")
        right = code.count("}")
        if right < left:
            code += "\n" + "}" * (left - right)
        return code


# to sanitize names for C# variables and Unity GameObjects.
def legalize_name(name):
    """Replaces illegal characters in C# variable/Unity GameObject names with underscores."""
    if not isinstance(name, str):
        name = str(name)
    return re.sub(r'[^0-9a-zA-Z_]', '_', name)


class EditorScriptGenerator:
    def __init__(self, bot):
        self.bot = bot

    def generate_editor_script(self, blueprint, asset_info):
        legal_name = legalize_name(blueprint['name'])
        class_name = f"{legal_name}AutoCreator"
        method_name = f"Create{legal_name}GO"

        # We define a few key API examples for the bot to learn from.
        # This is the "knowledge" we give to the bot.
        api_execution_examples = [
            "// Loading a prefab and instantiating it",
            "GameObject prefab = AssetDatabase.LoadAssetAtPath<GameObject>(\"Assets/Prefabs/MyPrefab.prefab\");",
            "GameObject newGO = (GameObject)PrefabUtility.InstantiatePrefab(prefab);",
            "",
            "// Creating a primitive sphere",
            "GameObject sphere = GameObject.CreatePrimitive(PrimitiveType.Sphere);",
            "",
            "// Finding an object by name and tag",
            "GameObject player = GameObject.Find(\"Player\");",
            "if (player == null) player = GameObject.FindGameObjectWithTag(\"Player\");",
            "",
            "// Setting transform properties",
            "newGO.transform.position = new Vector3(10f, 5f, 0f);",
            "newGO.transform.rotation = Quaternion.Euler(0f, 90f, 0f);",
            "newGO.transform.localScale = new Vector3(2f, 2f, 2f);",
            "",
            "// Adding a component to a GameObject",
            "newGO.AddComponent<Rigidbody>();",
            "",
            "// Getting a component and setting a public field",
            "CameraFollow cameraScript = cameraGO.GetComponent<CameraFollow>();",
            "if (cameraScript != null) cameraScript.target = player.transform;",
            "",
            "// Adding a tag and setting a layer",
            "TagHelper.AddTagIfNotExists(\"Player\");",
            "newGO.tag = \"Player\";",
            "newGO.layer = LayerMask.NameToLayer(\"Default\");",
            "",
            "// Selecting the newly created object in the editor",
            "Selection.activeGameObject = newGO;"
        ]

        # The core prompt is now a structured instruction for the bot.
        prompt = (
            f"You are a Unity C# Editor scripting expert. Generate a static C# script with a [MenuItem] to automatically create and set up a GameObject based on the following JSON blueprint. The script should be placed in the Assets/Editor/ folder.\n\n"
            f"**Blueprint:**\n{json.dumps(blueprint, indent=2, ensure_ascii=False)}\n\n"
            f"**Available Utility Classes:**\n"
            f"The project already contains a static class `TagHelper` with the method `AddTagIfNotExists(string tag)`. This method ensures a tag is available in the project before you assign it to a GameObject. You can call it directly like this: `TagHelper.AddTagIfNotExists(\"Player\");`.\n"
            f"The project also contains a static class `UIHelper` with the method `CreateText(string name, string text, Transform parent)`. You can use this to create UI Text objects.\n"
            f"The project also contains a static class `ReflectionHelper` with a single, unified method for safely setting script fields: **`SetValue(object obj, string fieldName, object value)`**. This method handles both reference and value types. You can use it like this: `ReflectionHelper.SetValue(patrolComp, \"scanAngle\", 90);`.\n\n"
            f"**Requirements:**\n"
            f"- The class name must be `{class_name}`.\n"
            f"- The method name must be `{method_name}` and should be a static void method decorated with `[MenuItem(\"Tools/Auto Attach/{legal_name}\")]`.\n"
            f"- Use `AssetDatabase.LoadAssetAtPath` to load prefabs and other assets.\n"
            f"- Correctly set all transform properties.\n"
            f"- **Using Directives:** At the top of the file, include `using UnityEngine;`, `using UnityEditor;`, and **most importantly, `using System.Linq;`** to access LINQ methods like `SelectMany` and `FirstOrDefault`.\n"
            f"- **IMPORTANT:** Iterate through the `components` list in the blueprint and use `go.AddComponent<T>()` to add each required component.\n"
            f"- **CRITICAL:** When assigning values to script fields, you MUST use the provided `ReflectionHelper` methods to ensure type safety and prevent runtime errors. Do NOT use `field.SetValue()` directly.\n"
            f"- **CRITICAL:** Do NOT redefine `TagHelper`, `UIHelper`, or `ReflectionHelper` or any other shared classes. Assume they are already defined in separate files and are accessible.\n"
            f"- Correctly assign all `script_fields`. For references like `Transform` or `GameObject`, use `GameObject.Find` or `GameObject.FindGameObjectWithTag` to locate the target object.\n"
            f"- Use `Selection.activeGameObject = ...` at the end to select the new object in the editor.\n"
            f"**Output:** Just the complete C# code block for the `{class_name}` class, without any comments, explanations, or markdown."
        )

        # Call the bot to generate the code.
        try:
            code = self.bot.ask(prompt)
            # Clean up the response, removing potential markdown blocks.
            code = re.sub(r"```csharp\n|```", "", code).strip()
            return code
        except Exception as e:
            print(f"Error generating editor script for {blueprint['name']}: {e}")
            return ""


class DebugBot:
    def __init__(self, bot):
        self.bot = bot

    def fix_scripts(self, script_error_list, problem_description=None, code_snippet=None):
        """
        Batch-fixes multiple C# scripts.
        script_error_list: [{'path':..., 'error':...}, ...]
        problem_description: (Optional) Overall problem description for the LLM
        code_snippet: (Optional) Reference code snippet for the LLM
        """
        # 1. Read all script source code
        scripts = []
        for entry in script_error_list:
            path = entry["path"]
            with open(path, "r", encoding="utf-8") as f:
                code = f.read()
            scripts.append({
                "path": path,
                "old_code": code,
                "error": entry["error"]
            })

        # 2. Construct Prompt
        prompt = "You are a Unity C# expert, tasked with automatically debugging and batch-fixing multiple scripts with pure code.\n"
        if problem_description:
            prompt += f"【Problem Description】\n{problem_description}\n"
        prompt += "Below are multiple scripts with errors. Please output the corrected full C# code for each of them.\n"
        for idx, script in enumerate(scripts, 1):
            prompt += (
                f"\n====== Script{idx} ======\n"
                f"【File Path】{script['path']}\n"
                f"【Current Code】\n{script['old_code']}\n"
                f"【Compilation Error Message】\n{script['error']}\n"
            )
        if code_snippet:
            prompt += (
                "\n【Reference Code Snippet, for automatic fixing】\n"
                f"{code_snippet}\n"
            )
        prompt += (
            "\nFor each script, please output only the corrected full C# script body. Do not include any comments, explanations, Markdown, code block markers, or extra content.\n"
            "Please match the output order with the script numbers above, using `====== Script1 ======`, followed immediately by the code body.\n"
        )

        # 3. LLM generates new code
        new_code = self.bot.ask(prompt)

        # 4. Parse LLM output & write back to file
        pattern = r"====== Script(\d+) ======\n(.*?)(?=\n====== Script\d+ ======|\Z)"
        matches = re.findall(pattern, new_code, flags=re.DOTALL)
        success = 0
        for idx, code in matches:
            idx = int(idx) - 1
            if 0 <= idx < len(scripts):
                out_path = scripts[idx]["path"]
                code_out = code.strip()
                code_out = re.sub(r"```[^\n]*\n?", "", code_out)
                left = code_out.count("{")
                right = code_out.count("}")
                if right < left:
                    code_out += "\n" + "}" * (left - right)
                with open(out_path, "w", encoding="utf-8") as f:
                    f.write(code_out)
                print(f"✅ Script fixed: {out_path}")
                success += 1
        if not success:
            print("⚠️ Failed to parse LLM output. Please check the prompt or LLM response format.")



def run_full_pipeline():
    bot = GPT4Bot("your_openai_key.txt")
    asset_info = {
        "models": [],
        "map":""
    }
    game_description = (
        "You are a Unity game development expert. Please generate a complete GameObject blueprint for a minimalist 3D obstacle course coin collection game. The creation method, components, scripts, and dependencies for each GameObject must be clearly defined.\n"
        "Requirements:\n"
        "1. All GameObjects must be created using Unity's basic primitive shapes (e.g., Sphere, Cube, Plane).\n"
        "2. The scene must contain the following objects:\n"
        "  - 🎥 main_camera: automatically follows the ball from a third-person perspective behind the ball.\n"
        "  - ⚽ ball:\n"
        "    - Press 'W' to move forward at constant speed.\n"
        "    - Press 'S' to move backward at constant speed.\n"
        "    - Press 'A' to move left at constant speed.\n"
        "    - Press 'D' to move right at constant speed.\n"
        "    - Collides with coin makes coin disappear.\n"
        "    - Falls off platform triggers game over.\n"
        "  - 💰 coin: multiple spinning coins (cubes tilted at angle) that rotate slowly on multiple axes.\n"
        "  - 🟦 plane: a square platform serving as the game area for ball movement and coin placement.\n"
        "3. Interaction Requirements:\n"
        "  - ⚽ ball movement controls (W/A/S/D) at constant speed.\n"
        "  - 💥 ball collides with coin: coin disappears and is collected.\n"
        "  - 📉 ball falls off platform: Game over.\n"
        "  - ✅ all coins collected: Game won.\n"
        "  - 🎥 main_camera follows ball's movement continuously.\n"
        "4. UI Requirements:\n"
        "  - Display WinText when all coins are collected.\n"
        "  - Display FailText when ball falls off platform.\n"
        "5. Each GameObject must clearly specify: name, create_type, asset_path, primitive_type, position, rotation, scale, tag, layer, components, scripts, script_fields.\n"
        "6. Automatically add Canvas, EventSystem, and UI components.\n"
    )

    # 1. Generate blueprints
    blueprint_gen = BlueprintGenerator(bot)
    blueprints = blueprint_gen.generate_blueprints(asset_info, game_description)
    blueprints = [bp for bp in blueprints if bp['name'].lower() not in {"wintext", "failtext", "uimanager"}]
    with open("gameobject_blueprints.json", "w", encoding="utf-8") as f:
        json.dump(blueprints, f, indent=2, ensure_ascii=False)
    print(f"✅ GameObject blueprints saved ({len(blueprints)} items)")

    # 2. Generate detailed script descriptions
    scripts_to_describe = [script for bp in blueprints for script in bp.get("scripts", [])]
    desc_gen = DescriptionGenerator(bot)
    script_descriptions = desc_gen.generate_script_descriptions(game_description, scripts_to_describe)
    print(f"✅ Generated detailed script descriptions.")

    # 3. Generate C# scripts
    # Get a list of all script names to be generated
    all_scripts_to_generate = []
    for bp in blueprints:
        all_scripts_to_generate.extend(bp.get("scripts", []))
    script_dir = "UnityProject/Assets/Scripts"
    os.makedirs(script_dir, exist_ok=True)
    csharp_script_gen = CSharpScriptGenerator(bot)
    for bp in blueprints:
        for script in bp.get("scripts", []):
            description = script_descriptions.get(script, "No detailed description found.")
            # MODIFICATION: Pass the new 'all_scripts_to_generate' list to the function
            code = csharp_script_gen.generate_script(
                bp['name'],
                script,
                description,
                bp.get("script_fields", {}).get(script, {}),
                all_scripts_to_generate  # <-- Add this parameter here
            )
            with open(os.path.join(script_dir, f"{script}.cs"), "w", encoding="utf-8") as f:
                f.write(code)
            print(f"✅ Script generated: {script}.cs")
    # 4. Generate Editor scripts (each GameObject in a separate .cs file)
    editor_dir = "UnityProject/Assets/Editor"
    os.makedirs(editor_dir, exist_ok=True)
    entry_methods = [
        "        UIManagerAutoCreator.CreateUIManagerGO();"
    ]
    editor_script_gen = EditorScriptGenerator(bot)
    for bp in blueprints:
        # Skip WinText/FailText/Canvas/UIManager, use the manually written templates directly
        if bp['name'].lower() in {"wintext", "failtext", "canvas", "uimanager"}:
            continue
        legal_name = legalize_name(bp['name'])
        class_name = f"{legal_name}AutoCreator"
        method_name = f"Create{legal_name}GO"
        cs_code = editor_script_gen.generate_editor_script(bp, asset_info)  # Use the new bot-driven generator
        cs_filename = f"{class_name}.cs"
        with open(os.path.join(editor_dir, cs_filename), "w", encoding="utf-8") as f:
            f.write(cs_code)
        print(f"✅ Editor script generated: {cs_filename}")
        entry_methods.append(f"        {class_name}.{method_name}();")

    # 5. Generate a unified entry point
    autoattach_code = f"""using UnityEditor;
        using UnityEngine;
        using UnityEditor.SceneManagement;

        public static class AutoAttachAll
        {{
            [MenuItem("Tools/Auto Attach/All")]
            public static void AttachAll()
            {{
                EditorSceneManager.NewScene(NewSceneSetup.DefaultGameObjects);
        {chr(10).join(entry_methods)}
                Debug.Log("✅ All GameObjects and components have been created and attached.");
            }}
        }}
        """
    with open(os.path.join(editor_dir, "AutoAttachAll.cs"), "w", encoding="utf-8") as f:
        f.write(autoattach_code)
    print("✅ Unified Editor auto-attach script generated: AutoAttachAll.cs")


def reorder_autoattachall(autoattach_path, gpt_key_path="your_openai_key.txt"):
    # 1. Read the original code
    with open(autoattach_path, "r", encoding="utf-8") as f:
        code = f.read()

    # 2. Extract all attach function calls (regardless of leading/trailing spaces)
    call_pattern = re.compile(r'^\s*([A-Za-z0-9_]+AutoCreator\.Create[A-Za-z0-9_]+GO\(\);)', re.MULTILINE)
    calls = call_pattern.findall(code)
    if not calls:
        print("No AutoCreator attach function calls found. Exiting.")
        return

    # 3. Ask GPT for a suggested order
    prompt = (
            "You are a Unity level automation expert. A list of Unity Editor script function calls to create game objects is provided below. These functions must be called in a specific order due to dependencies. For example, a script that references another object must be created after the object it depends on has been instantiated.\n\n"
            "**Creation Calls:**\n"
            + "\n".join(calls) +
            "\n\n"
            "**Dependency Rules:**\n"
            "- **UI:** Canvas, UI Manager, WinText, and FailText must be created first to be available for other scripts to reference.\n"
            "- **Player:** The Player object (JohnLemon) must be created before the Camera, as the Camera will follow the Player.\n"
            "- **Enemies:** Enemies (Ghost, Gargoyle) can be created independently of the player but must be available if the player's script needs to find them.\n"
            "- **Level:** The map prefab (`Level`) should be instantiated first to provide a physical space for other objects to be placed within.\n"
            "- **Event System:** The Event System can be created at any point but is typically created early with the Canvas.\n"
            "\n"
            "Please analyze the provided list of creation calls and reorder them to respect these dependency rules. Do not include any extra text, comments, or explanations. Just output the final, corrected list of function calls, with one function call per line."
    )
    bot = GPT4Bot(gpt_key_path)
    gpt_reply = bot.ask(prompt).strip()

    # 4. Parse GPT's output
    if "The order is already logical" in gpt_reply:
        print("The order is already logical, no changes needed.")
        return
    new_calls = [line.strip() for line in gpt_reply.splitlines() if line.strip() in calls]
    if not new_calls:
        print("GPT did not provide a valid order. The original order will be kept.")
        return
    # Keep function calls not returned by GPT (e.g., if GPT missed one) and append them to the end
    rest_calls = [c for c in calls if c not in new_calls]
    all_calls = new_calls + rest_calls

    # 5. Replace the call order in the AttachAll() function
    def replace_attachall_block(code, call_list):
        pattern = re.compile(
            r'public\s+static\s+void\s+AttachAll\s*\(\)\s*\{(.*?)(Debug\.Log\([^)]+\);)', re.DOTALL
        )
        m = pattern.search(code)
        if not m:
            print("Could not find the AttachAll method body.")
            return code
        before = m.group(1)
        debug_log = m.group(2)
        # Replace all attach calls (keep indentation)
        new_block = '\n'
        for c in call_list:
            new_block += f'        {c}\n'
        new_block += f'        {debug_log}\n'
        new_code = code[:m.start(1)] + new_block + code[m.end(2):]
        return new_code

    new_code = replace_attachall_block(code, all_calls)

    # 6. Write back to file
    with open(autoattach_path, "w", encoding="utf-8") as f:
        f.write(new_code)
    print(f"✅ AutoAttachAll.cs has been automatically reordered and saved based on GPT's suggestion!")



def run_debug_bot_multi():
    bot = GPT4Bot("your_openai_key.txt")
    debug_bot = DebugBot(bot)
    print(
        "🔎 Please enter Unity error content, problem description, and a list of script paths to batch-fix related C# scripts.")
    while True:
        print("\n--------------------")
        problem_description = input(
            "Please describe the problem you are encountering (e.g., type/reference conflicts involving multiple scripts, design requirements; can be left blank):\n")
        error_num = int(input("How many scripts need to be fixed? Enter the number: "))
        script_error_list = []
        for i in range(error_num):
            print(f"\n--- Script {i + 1} ---")
            error_message = input("Please enter the Unity compilation error content (paste the full error message):\n")
            script_path = input(
                "Please enter the relative path of the faulty script (e.g., Assets/Scripts/BallController.cs):\n")
            if not script_path.startswith("UnityProject/"):
                script_path = os.path.join("UnityProject", script_path)
            if not os.path.exists(script_path):
                print(f"❌ File not found: {script_path}")
                continue
            script_error_list.append({"path": script_path, "error": error_message})

        # The code snippet you provided needs to be defined within the function scope to be used
        code_snippet = """
        GameObject PlayerGO = GameObject.Find("Player");
        if (PlayerGO == null) {
            PlayerGO = GameObject.FindGameObjectWithTag("Player");
        }
        var comp_CameraFollow_target = MainCameraGO.GetComponent<CameraFollow>();
        if (comp_CameraFollow_target != null && PlayerGO != null) {
            comp_CameraFollow_target.target = PlayerGO.transform;
        }
        """.strip()

        code_snippet = code_snippet.strip() if code_snippet else None

        debug_bot.fix_scripts(script_error_list, problem_description=problem_description, code_snippet=code_snippet)
        cont = input("Do you want to continue fixing the next batch? (y/n): ")
        if cont.lower() != "y":
            break


if __name__ == "__main__":
    run_full_pipeline()
    reorder_autoattachall(
        autoattach_path="UnityProject/Assets/Editor/AutoAttachAll.cs",
        gpt_key_path="your_openai_key.txt"
    )
    run_debug_bot_multi()