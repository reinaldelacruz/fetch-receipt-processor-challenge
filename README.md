# Fetch Take-Home Challenge

## Overview
A simple Django web service that allows users to process receipt data and retrieve reward points associated with those receipts. The service provides two main endpoints: one for submitting receipts and generating unique IDs, and another for retrieving the points associated with a specific receipt ID.

## Endpoints

### 1. Process Receipts

- **Path**: `/receipts/process`  
- **Method**: `POST`  
- **Payload**: Receipt JSON  
- **Response**: JSON containing a generated `id` for the receipt

**Description**:  
Accepts a JSON object representing a receipt, processes it, and returns a unique ID associated with the receipt.

---

### 2. Get Points

- **Path**: `/receipts/{id}/points`  
- **Method**: `GET`  
- **Response**: JSON object containing the number of points awarded for the receipt

**Description**:  
Retrieves the number of points awarded for a given receipt using its ID.

---

## Running the App

Follow these steps to set up and run the Django app locally:

### 1. Clone the Repository

```bash
git clone https://github.com/reinaldelacruz/fetch-receipt-processor-challenge.git
cd fetch-receipt-processor-challenge
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Run the Development Server
```bash
python manage.py runserver
```

