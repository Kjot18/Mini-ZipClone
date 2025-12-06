import { gql } from '@apollo/client';

export const REGISTER = gql`
  mutation Register($input: RegisterInput!) {
    register(input: $input) {
      token
      user {
        id
        username
        email
        full_name
        role
      }
    }
  }
`;

export const LOGIN = gql`
  mutation Login($input: LoginInput!) {
    login(input: $input) {
      token
      user {
        id
        username
        email
        full_name
        role
      }
    }
  }
`;

export const CREATE_PURCHASE_REQUEST = gql`
  mutation CreatePurchaseRequest($input: PurchaseRequestInput!) {
    createPurchaseRequest(input: $input) {
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
      }
    }
  }
`;

export const APPROVE_REQUEST = gql`
  mutation ApproveRequest($input: ApprovalInput!) {
    approveRequest(input: $input) {
      id
      status
      comment
      stage
      purchase_request_id
      approver {
        id
        username
        full_name
      }
    }
  }
`;

