# Task 1: Add Yourself to the Notable Mentions

## 🎯 Objective  
Practice the **Git & GitHub workflow**: clone, branch, commit, push, and create a Pull Request (PR).

## 💡 Idea  
You’ll add your personal details to the repository by creating a new text file inside the `notable-mention/` folder.

---

## 🚀 Steps  

1. **Go to the repository**  
   👉 [robotics-core-workshop-oct2025](https://github.com/Bakel-Bakel/robotics-core-workshop-oct2025)

2. **Fork the repository**  
   - Click the **Fork** button on GitHub to create your copy.

3. **Clone your fork to your local machine**  
   ```bash
   git clone https://github.com/<your-username>/robotics-core-workshop-oct2025.git
   cd robotics-core-workshop-oct2025
   ```

4. **Create a new branch with your name**  
   ```bash
   git checkout -b add-yourname
   ```

5. **Navigate to the folder**  
   ```bash
   cd notable-mention
   ```

6. **Create your text file and add your details**  
   - File format: `Firstname-Lastname.txt`  
   - Example:  
     ```
     Bakel-Bakel.txt
     ```

   - Inside the file, add your details in this format:  
     ```
     Full-Name , Linkedin-url , Role (student)
     ```

7. **Stage and commit your file**  
   ```bash
   git add notable-mention/Firstname-Lastname.txt
   git commit -m "Add my name to notable mentions"
   ```

8. **Push your branch**  
   ```bash
   git push origin add-yourname
   ```

9. **Create a Pull Request**  
   - Go to your fork on GitHub.  
   - Open a Pull Request from your branch → **main repository**.

---

## ✅ Completion Criteria  

- A `.txt` file is added in the `notable-mention/` folder.  
- The file contains your full name and LinkedIn link.  
- A Pull Request is submitted and visible on the original repository.  

---

📌 That’s it! You’ve successfully contributed your first Pull Request 🎉
