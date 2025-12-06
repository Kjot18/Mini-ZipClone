# GraphQL API Examples

## Queries

### Get All Purchase Requests

```graphql
query {
  purchaseRequests {
    id
    title
    description
    amount
    currency
    status
    created_at
    requester {
      id
      username
      email
    }
    approvals {
      id
      status
      comment
      stage
      approver {
        username
      }
    }
  }
}
```

### Get Purchase Request by ID

```graphql
query {
  purchaseRequest(id: 1) {
    id
    title
    description
    amount
    status
    requester {
      username
      email
    }
    approvals {
      status
      comment
      approver {
        username
      }
    }
  }
}
```

### Get All Users

```graphql
query {
  users {
    id
    username
    email
    role
  }
}
```

### Get Approvals

```graphql
query {
  approvals(purchaseRequestId: 1) {
    id
    status
    comment
    stage
    approver {
      username
    }
  }
}
```

## Mutations

### Register User

```graphql
mutation {
  register(input: {
    username: "newuser"
    email: "newuser@example.com"
    password: "password123"
    full_name: "New User"
  }) {
    token
    user {
      id
      username
      email
      role
    }
  }
}
```

### Login

```graphql
mutation {
  login(input: {
    username: "user"
    password: "user123"
  }) {
    token
    user {
      id
      username
      email
      role
    }
  }
}
```

### Create Purchase Request

```graphql
mutation {
  createPurchaseRequest(input: {
    title: "Office Supplies"
    description: "Need new office supplies"
    amount: 500.00
    currency: "USD"
  }) {
    id
    title
    status
    amount
  }
}
```

### Approve/Deny Request

```graphql
mutation {
  approveRequest(input: {
    purchase_request_id: 1
    status: "approved"
    comment: "Looks good!"
  }) {
    id
    status
    comment
    purchase_request_id
  }
}
```

