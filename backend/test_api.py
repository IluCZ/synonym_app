# test_api.py
import asyncio
import httpx
import json
from datetime import datetime
from typing import Dict, Optional

class SynonymTester:
    def __init__(self):
        self.api_url = "http://localhost:8000/synonyms"
        self.single_word_tests = [
            # Common words
            "happy",
            "car",
            "fast",
            "big",
            "house",
            
            # Technical terms
            "programming",
            "computer",
            "software",
            
            # Adjectives
            "beautiful",
            "extraordinary",
            "intelligent",
            
            # Nouns
            "dog",
            "garden",
            "water",
            
            # Verbs
            "run",
            "jump",
            "write"
        ]
        
        self.word_pairs = [
            ("fast", "car"),
            ("big", "house"),
            ("beautiful", "garden"),
            ("dark", "night"),
            ("small", "dog"),
            ("running", "water")
        ]

    async def test_single_word(self, word: str, min_synonyms: int = 3, max_synonyms: int = 10) -> Dict:
        """Test the API with a single word"""
        print(f"\nTesting single word: '{word}'")
        print("-" * 50)
        
        try:
            async with httpx.AsyncClient() as client:
                start_time = datetime.now()
                response = await client.post(
                    self.api_url,
                    json={
                        "word": word,
                        "min_synonyms": min_synonyms,
                        "max_synonyms": max_synonyms
                    }
                )
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                
                print(f"Status Code: {response.status_code}")
                print(f"Response Time: {response_time:.2f} seconds")
                
                if response.status_code == 200:
                    result = response.json()
                    print("\nSynonyms found:")
                    for i, synonym in enumerate(result["synonyms"], 1):
                        print(f"{i}. {synonym}")
                    print(f"\nSources used: {', '.join(result['sources'])}")
                    print(f"Total synonyms: {len(result['synonyms'])}")
                    
                    return {
                        "success": True,
                        "status_code": response.status_code,
                        "response_time": response_time,
                        "synonyms_count": len(result["synonyms"]),
                        "sources": result["sources"]
                    }
                else:
                    print(f"Error: {response.text}")
                    return {
                        "success": False,
                        "status_code": response.status_code,
                        "error": response.text
                    }
                    
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def test_word_pair(self, word1: str, word2: str) -> Dict:
        """Test the API with a word pair"""
        print(f"\nTesting word pair: '{word1} {word2}'")
        print("-" * 50)
        
        try:
            async with httpx.AsyncClient() as client:
                start_time = datetime.now()
                response = await client.post(
                    self.api_url,
                    json={
                        "word": word1,
                        "second_word": word2,
                        "max_synonyms": 10
                    }
                )
                end_time = datetime.now()
                response_time = (end_time - start_time).total_seconds()
                
                print(f"Status Code: {response.status_code}")
                print(f"Response Time: {response_time:.2f} seconds")
                
                if response.status_code == 200:
                    result = response.json()
                    
                    print(f"\nSynonyms for '{word1}':")
                    for i, synonym in enumerate(result["synonyms"], 1):
                        print(f"{i}. {synonym}")
                        
                    if result.get("second_word_synonyms"):
                        print(f"\nSynonyms for '{word2}':")
                        for i, synonym in enumerate(result["second_word_synonyms"], 1):
                            print(f"{i}. {synonym}")
                    
                    print(f"\nSources used: {', '.join(result['sources'])}")
                    
                    return {
                        "success": True,
                        "status_code": response.status_code,
                        "response_time": response_time,
                        "first_word_count": len(result["synonyms"]),
                        "second_word_count": len(result.get("second_word_synonyms", [])),
                        "sources": result["sources"]
                    }
                else:
                    print(f"Error: {response.text}")
                    return {
                        "success": False,
                        "status_code": response.status_code,
                        "error": response.text
                    }
                    
        except Exception as e:
            print(f"Error occurred: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }

    async def run_tests(self):
        """Run all tests and generate summary"""
        print("Starting Synonym API Tests...")
        print("=" * 60)
        
        # Test single words
        single_word_results = []
        for word in self.single_word_tests:
            result = await self.test_single_word(word)
            single_word_results.append({"word": word, "result": result})
            print("\n" + "="*60)
        
        # Test word pairs
        word_pair_results = []
        for word1, word2 in self.word_pairs:
            result = await self.test_word_pair(word1, word2)
            word_pair_results.append({
                "word1": word1,
                "word2": word2,
                "result": result
            })
            print("\n" + "="*60)
        
        # Generate summary
        print("\nTest Summary")
        print("=" * 60)
        
        # Single word summary
        print("\nSingle Word Tests:")
        successful_single = sum(1 for r in single_word_results if r["result"]["success"])
        print(f"Total tests: {len(single_word_results)}")
        print(f"Successful: {successful_single}")
        print(f"Failed: {len(single_word_results) - successful_single}")
        
        # Word pair summary
        print("\nWord Pair Tests:")
        successful_pairs = sum(1 for r in word_pair_results if r["result"]["success"])
        print(f"Total tests: {len(word_pair_results)}")
        print(f"Successful: {successful_pairs}")
        print(f"Failed: {len(word_pair_results) - successful_pairs}")
        
        # Calculate average response times
        single_times = [r["result"]["response_time"] for r in single_word_results 
                       if r["result"]["success"] and "response_time" in r["result"]]
        pair_times = [r["result"]["response_time"] for r in word_pair_results 
                     if r["result"]["success"] and "response_time" in r["result"]]
        
        if single_times:
            avg_single = sum(single_times) / len(single_times)
            print(f"\nAverage single word response time: {avg_single:.2f} seconds")
        if pair_times:
            avg_pair = sum(pair_times) / len(pair_times)
            print(f"Average word pair response time: {avg_pair:.2f} seconds")
        
        # API source usage statistics
        source_usage = {}
        for r in single_word_results + word_pair_results:
            if r["result"]["success"] and "sources" in r["result"]:
                for source in r["result"]["sources"]:
                    source_usage[source] = source_usage.get(source, 0) + 1
        
        print("\nAPI Source Usage:")
        for source, count in source_usage.items():
            print(f"{source}: {count} times")
        
        # Print failed test details
        failed_tests = (
            [r for r in single_word_results if not r["result"]["success"]] +
            [r for r in word_pair_results if not r["result"]["success"]]
        )
        
        if failed_tests:
            print("\nFailed Tests Details:")
            print("=" * 60)
            for test in failed_tests:
                if "word" in test:  # Single word test
                    print(f"\nWord: {test['word']}")
                else:  # Word pair test
                    print(f"\nWord Pair: {test['word1']} {test['word2']}")
                print(f"Error: {test['result'].get('error', 'Unknown error')}")

if __name__ == "__main__":
    print("Starting Synonym API Tests...")
    print("Make sure your FastAPI server is running on http://localhost:8000")
    print("=" * 60)
    
    tester = SynonymTester()
    asyncio.run(tester.run_tests())