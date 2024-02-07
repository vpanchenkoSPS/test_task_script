# Test Task Script

ToDo:
Setup mock endpoint so you will be able to work with it later
Retrieve marketplace data from previously created url

Find all sellers that have at least 2 products with price above 100. Print sellers and this products.

### Requirements:

Assume, sometimes endpoint can return some errors, so your code needs to handle them (some of them needs to be retried):
- 400: Bad Request
- 404: No marketplace found
- 500: Internal Server Error

Call to external service needs to have 60 second time limit.

### Nice to have:
- Ability to configure retries.
- At least 1 test, cover what you think is most crucial


### While working on this task were used:
 - [Mockaroo](https://mockaroo.com/) create a test data
 - [Mockbin](https://mockbin.io/) test API calls

---

### How to Use the Project:
1) Use already created test_data file or creating your own json data that represent your own market with similar data to fields below by using [Mockaroo](https://mockaroo.com/) for creating endpoint:
    - [
        - {"id":1,
        - "seller_first_name":"Samara",
        - "seller_last_name":"Hebbes",
        - "products": [{
          - "id": 1,
          - "product_name": "Wine - Cava Aria Estate Brut",
          - "product_quantity": 7,
          - "product_price": 85
      }],
        - "rating":4.31},]
2) Open [Mockbin](https://mockbin.io/) paste market data to the 'Body'
3) Copy API url and paste It to the resources/configuration.py/MOCK_ENDPOINT_URL
4) To run the project you can use 'Run' function at the main.py file or use terminal (Windows)
    ``` 
    python main.py 
    ``` 