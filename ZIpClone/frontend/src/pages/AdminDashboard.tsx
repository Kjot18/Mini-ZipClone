import React, { useState } from 'react';
import { useQuery, useMutation } from '@apollo/client';
import { GET_PURCHASE_REQUESTS } from '../graphql/queries';
import { APPROVE_REQUEST } from '../graphql/mutations';
import '../App.css';

interface ApprovalModalProps {
  requestId: number;
  onClose: () => void;
  onApprove: (status: string, comment: string) => void;
}

const ApprovalModal: React.FC<ApprovalModalProps> = ({ requestId, onClose, onApprove }) => {
  const [status, setStatus] = useState('approved');
  const [comment, setComment] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onApprove(status, comment);
  };

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
    }}>
      <div className="card" style={{ maxWidth: '500px', width: '90%' }}>
        <h3>Approve/Deny Request</h3>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Decision</label>
            <select
              value={status}
              onChange={(e) => setStatus(e.target.value)}
              style={{ width: '100%', padding: '10px' }}
            >
              <option value="approved">Approve</option>
              <option value="denied">Deny</option>
            </select>
          </div>
          <div className="form-group">
            <label>Comment</label>
            <textarea
              value={comment}
              onChange={(e) => setComment(e.target.value)}
              placeholder="Add a comment (optional)"
            />
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button type="submit" className={`btn ${status === 'approved' ? 'btn-success' : 'btn-danger'}`}>
              {status === 'approved' ? 'Approve' : 'Deny'}
            </button>
            <button type="button" className="btn btn-secondary" onClick={onClose}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

const AdminDashboard: React.FC = () => {
  const [selectedRequest, setSelectedRequest] = useState<number | null>(null);
  const { loading, error, data, refetch } = useQuery(GET_PURCHASE_REQUESTS);
  const [approveRequest, { loading: approving }] = useMutation(APPROVE_REQUEST, {
    refetchQueries: [{ query: GET_PURCHASE_REQUESTS }],
  });

  if (loading) return <div className="container">Loading...</div>;
  if (error) return <div className="container">Error: {error.message}</div>;

  const requests = data?.purchaseRequests || [];

  const handleApprove = async (status: string, comment: string) => {
    if (!selectedRequest) return;

    try {
      await approveRequest({
        variables: {
          input: {
            purchase_request_id: selectedRequest,
            status,
            comment: comment || null,
          },
        },
      });
      setSelectedRequest(null);
      refetch();
    } catch (err: any) {
      alert(err.message || 'Failed to update request');
    }
  };

  const getStatusClass = (status: string) => {
    return `status-badge status-${status.toLowerCase().replace(' ', '_')}`;
  };

  const pendingRequests = requests.filter((r: any) => 
    r.status === 'pending' || r.status === 'in_review'
  );

  return (
    <div className="container">
      <h1>Admin Dashboard</h1>
      
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        <div className="card" style={{ flex: 1 }}>
          <h3>Total Requests</h3>
          <p style={{ fontSize: '2rem', margin: 0 }}>{requests.length}</p>
        </div>
        <div className="card" style={{ flex: 1 }}>
          <h3>Pending Approval</h3>
          <p style={{ fontSize: '2rem', margin: 0 }}>{pendingRequests.length}</p>
        </div>
      </div>

      <div className="card">
        <h2>All Purchase Requests</h2>
        {requests.length === 0 ? (
          <p>No purchase requests yet.</p>
        ) : (
          <table className="table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Requester</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {requests.map((request: any) => (
                <tr key={request.id}>
                  <td>{request.id}</td>
                  <td>{request.title}</td>
                  <td>{request.requester?.username || 'N/A'}</td>
                  <td>{request.currency} {request.amount.toFixed(2)}</td>
                  <td>
                    <span className={getStatusClass(request.status)}>
                      {request.status}
                    </span>
                  </td>
                  <td>{new Date(request.created_at).toLocaleDateString()}</td>
                  <td>
                    {(request.status === 'pending' || request.status === 'in_review') && (
                      <button
                        className="btn btn-primary"
                        onClick={() => setSelectedRequest(request.id)}
                        style={{ marginRight: '10px' }}
                      >
                        Review
                      </button>
                    )}
                    <button
                      className="btn btn-secondary"
                      onClick={() => {
                        alert(`Request Details:\n\nTitle: ${request.title}\nDescription: ${request.description || 'N/A'}\nAmount: ${request.currency} ${request.amount}\nStatus: ${request.status}\n\nApprovals: ${request.approvals?.length || 0}`);
                      }}
                    >
                      View Details
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {selectedRequest && (
        <ApprovalModal
          requestId={selectedRequest}
          onClose={() => setSelectedRequest(null)}
          onApprove={handleApprove}
        />
      )}
    </div>
  );
};

export default AdminDashboard;

