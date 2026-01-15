# Mental Health Chatbot

## Steps to Run

1. Create a Python virtual environment:
   ```
   python -m venv myenv
   ```

2. Activate the virtual environment:
   - Windows:
     ```
     myenv\Scripts\activate
     ```
   - Linux/Mac:
     ```
     source myenv/bin/activate
     ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Get your Google API key from [Google AI Studio](https://aistudio.google.com/) and create a `.env` file in the project root with:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

5. Run the server:
   ```
   python ChatbotServer.py
   ```

6. In a new terminal, run the test:
   ```
   python test.py
   ```
