# Running the Tests

1. Make sure your application is running and accessible at:
   - Frontend: http://localhost:8501
   - Backend: http://localhost:8000

2. Open a new terminal window

3. Navigate to your test directory:
   ```bash
   cd synonym_app/tests  # or wherever your test_api.py is located
   ```

4. Run the test script:
   ```bash
   python test_api.py
   ```

# Expected Output
The script will run through:
- 17 single word tests
- 6 word pair tests

You should see:
- Individual test results for each word/pair
- Response times
- Status codes
- Number of synonyms found
- Sources used
- A comprehensive summary at the end

# Troubleshooting
If you see connection errors:
1. Verify the backend is running (`http://localhost:8000/health`)
2. Check Docker logs for any errors
3. Ensure no firewall is blocking the connection

# Test Categories Covered
1. Single Words:
   - Common words (happy, car, etc.)
   - Technical terms (programming, computer)
   - Different parts of speech (nouns, verbs, adjectives)

2. Word Pairs:
   - Common combinations (fast car, big house)
   - Descriptive pairs (beautiful garden)
   - Abstract combinations (dark night)