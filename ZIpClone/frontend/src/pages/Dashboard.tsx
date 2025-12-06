import React from 'react';
import { useQuery } from '@apollo/client';
import { Link } from 'react-router-dom';
import { GET_PURCHASE_REQUESTS } from '../graphql/queries';
import '../App.css';

const Dashboard: React.FC = () => {
  const userStr = localStorage.getItem('user');
  const user = userStr ? JSON.parse(userStr) : null;
  const userId = user?.id;

  const { loading, error, data, refetch } = useQuery(GET_PURCHASE_REQUESTS, {
    variables: { requesterId: userId },
    skip: !userId,
  });

  if (loading) return <div className="container">Loading...</div>;
  if (error) return <div className="container">Error: {error.message}</div>;

  const requests = data?.purchaseRequests || [];

  const getStatusClass = (status: string) => {
    return `status-badge status-${status.toLowerCase().replace(' ', '_')}`;
  };

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h1>My Purchase Requests</h1>
        <Link to="/request" className="btn btn-primary">
          New Request
        </Link>
      </div>

      {requests.length === 0 ? (
        <div className="card">
          <p>No purchase requests yet. <Link to="/request">Create your first request</Link></p>
        </div>
      ) : (
        <div className="card">
          <table className="table">
            <thead>
              <tr>
                <th>Title</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Created</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {requests.map((request: any) => (
                <tr key={request.id}>
                  <td>{request.title}</td>
                  <td>{request.currency} {request.amount.toFixed(2)}</td>
                  <td>
                    <span className={getStatusClass(request.status)}>
                      {request.status}
                    </span>
                  </td>
                  <td>{new Date(request.created_at).toLocaleDateString()}</td>
                  <td>
                    <Link to={`/request/${request.id}`}>View</Link>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

