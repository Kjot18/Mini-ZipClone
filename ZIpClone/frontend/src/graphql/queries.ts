import { gql } from '@apollo/client';

export const GET_PURCHASE_REQUESTS = gql`
  query GetPurchaseRequests($status: String, $requesterId: Int) {
    purchaseRequests(status: $status, requesterId: $requesterId) {
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
        full_name
        email
      }
      approvals {
        id
        status
        comment
        stage
        created_at
        approver {
          id
          username
          full_name
        }
      }
    }
  }
`;

export const GET_PURCHASE_REQUEST = gql`
  query GetPurchaseRequest($id: Int!) {
    purchaseRequest(id: $id) {
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
        full_name
        email
      }
      approvals {
        id
        status
        comment
        stage
        created_at
        approver {
          id
          username
          full_name
        }
      }
    }
  }
`;

export const GET_APPROVALS = gql`
  query GetApprovals($purchaseRequestId: Int) {
    approvals(purchaseRequestId: $purchaseRequestId) {
      id
      purchase_request_id
      status
      comment
      stage
      created_at
      approver {
        id
        username
        full_name
      }
    }
  }
`;

