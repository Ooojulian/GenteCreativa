// PrivateRoute.jsx
import React from 'react';
import { Navigate, Route, RouteProps } from 'react-router-dom'; // Cambia 'Route'
import { useAuth } from '../../contexts/AuthContext';

interface PrivateRouteProps extends RouteProps {
    children: React.ReactNode;
  }

const PrivateRoute: React.FC<PrivateRouteProps> = ({ children, ...rest }) => {
  const { isAuthenticated } = useAuth();

  return (
    <Route
        {...rest}
        element = {isAuthenticated ? children : <Navigate to="/login" replace />}
    />
  );
};

export default PrivateRoute;
