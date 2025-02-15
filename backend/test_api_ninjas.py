# test_api_ninjas.py
import httpx
import asyncio

async def test_api_ninjas():
    url = "https://api.api-ninjas.com/v1/thesaurus"
    headers = {
        "X-Api-Key": "oFp6FIbNI+5DQGSfDkmMag==0UFNr61a8PcsRKDm",
        "accept": "application/json"
    }
    params = {"word": "dog"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, params=params)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_api_ninjas())