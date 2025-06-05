# INDIAN SIGN LANGUAGE TRANSLATOR - SIGNSPIRE

Absolutely! Here's a **descriptive and polished `README.md`** for your **SignSpire** project, without directory structure and with a clear explanation of the system, features, and how to use it:

---

````markdown
# ✨ SignSpire: 2D Indian Sign Language Translator

**SignSpire** is an innovative project that bridges the communication gap between the hearing-impaired community and the rest of the world. It translates natural language text into **Indian Sign Language (ISL)** and visualizes it through animated 2D **stickman figures**, using a coordinate-based pose system.

---

## 🧠 What is SignSpire?

SignSpire converts English text into ISL by:
- Breaking the sentence into individual words.
- Mapping each word to a predefined `.pose` file that describes body joint positions over time.
- Animating the sequence using a stickman representation.
- Creating a seamless, continuous animation with smooth transitions between gestures.

The result is an easy-to-understand animated video that accurately reflects Indian Sign Language for the input sentence.

---

## 🎯 Key Features

- 🗣 **Text to Sign Language**: Converts any input sentence into ISL.
- 🔄 **Pose-Based System**: Uses `.pose` files that contain frame-by-frame joint coordinates.
- 🧍‍♂️ **Stickman Animation**: Clean 2D visualization using stick figures to represent hand and body movement.
- 🌀 **Smooth Transitions**: Adds blending and hold frames between signs for natural flow.
- 🎥 **Video Output**: Final ISL animation is exported as an `.mp4` video.

---

## 📁 How Pose Files Work

Each `.pose` file corresponds to a single word in ISL and contains joint positions for a stickman over multiple frames. A typical `.pose` file holds coordinates for:
- Head
- Hands
- Elbows
- Shoulders
- Torso
- Legs (optional for some gestures)

The animation engine reads this file, draws each frame, and then stitches them together with transitions to form a smooth gesture sequence.

---

## 🚀 How to Use SignSpire

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/your-username/signspire.git
   cd signspire
````

2. **Install Requirements**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Translator**

   ```bash
   python main.py "Hello how are you"
   ```

4. **Get the Output**
   The animated ISL video will be saved automatically as an `.mp4` file in the output folder.

---

## 🧪 Example Input & Output

**Input**:

```
"Hello how are you"
```

**Output**:
An animation where the stickman performs ISL gestures for:

* "Hello"
* "How"
* "Are you"
  With natural transitions between them.

---

## 🔧 Technologies Used

* **FastAPI**
* **MediaPipe** – Extraction of pose from video
* **Pose-format** – Stickman drawing
* **Cloudinary** –Storing .pose files


---

## 🌟 Why Stickman?

Using a 2D stickman ensures:

* Clarity of gestures
* Lightweight rendering
* Faster processing
* Easy debugging and extension

It also makes the system ideal for web deployment, mobile usage, or integration into assistive tools.

---

## 📌 Future Goals

* 🔤 Add sentence-level ISL grammar conversion
* 🤖 Integrate NLP to improve word mapping
* 🌐 Deploy as a web app using Flask + React
* 🤲 Support more ISL vocabulary
* 👤 Use skeletal tracking for real-time ISL learning

---

## 🤝 Contribute

You can help by:

* Contributing more `.pose` files
* Improving animation logic
* Creating better UI/UX for accessibility
* Optimizing performance for mobile and browser use

---


