## Setting Up VYAPAARSAHAYAK

### Terminal 1: (for backend)

1. Navigate to the backend directory:

    ```bash
    cd gen-ai-project/backend/fastapibackend 
    ```

2. Create a virtual environment:

    ```bash
    python -m venv myvenv
    ```

3. Activate the virtual environment:

    ```bash
    cd myvenv/Scripts
  
    ```
    ```bash
    ./Activate
    ```

4. Go back to the project directory:

    ```bash
    cd ../..
    ```

5. Install required packages:

    ```bash
    pip install -r requirements.txt
    ```

6. Run the backend server:

    ```bash
    uvicorn main:app --reload
    ```

### Terminal 2: (for frontend)

1. Navigate to the frontend directory:

    ```bash
    cd gen-ai-project/frontend/gen-ai
    ```

2. Install dependencies:

    ```bash
    npm install
    ```

3. Start the development server:

    ```bash
    npm run dev
    ```



## Setting Up ChatApp

1. download dependencies:

    ```bash
    npm install firebase
    npm install universal-cookie
    ```
2. start the app

    ```bash
    npm run
    ```

3. firebase-config

    ```bash
    add your own key!!
    ```
