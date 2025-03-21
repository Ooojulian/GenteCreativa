// frontend/src/components/Dashboard/Dashboard.tsx
import React, { useState, useEffect } from 'react';
import { getPedidos, iniciarPedido, finalizarPedido } from '../../services/api';
import PedidoItem from './PedidoItem';
import { useAuth } from '../../context/AuthContext'; // Usa el hook useAuth
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const [pedidos, setPedidos] = useState<any[]>([]); // Usa un tipo más específico si tienes la interfaz de Pedido
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user, logOut } = useAuth(); // Usar el hook, mucho más limpio
    const navigate = useNavigate();


    const fetchPedidos = async () => {
        try {
            const data = await getPedidos();
            setPedidos(data);
        } catch (error:any) {
            setError(error.message || 'Error al cargar los pedidos.');
        } finally {
            setLoading(false);
        }
    };

  useEffect(() => {


    if (user && user.rol === 'conductor') {
      fetchPedidos();
    }else if(user){
        navigate('/login');
    }

  }, [user, navigate]); // user y navigate como dependencias.  MUY importante.


    const handleLogout = () => {
        logOut();
        navigate('/login');
    }


  if (loading) {
    return <div>Cargando...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }
  if(!user || user.rol !== 'conductor'){
    return (
        <div>
            <h2>Acceso Denegado</h2>
            <p>Debes tener el rol de conductor para ver esta página</p>
        </div>
    )
  }

  return (
    <div>
      <h2>Pedidos Asignados</h2>
      <button onClick={handleLogout}>Cerrar sesión</button>
      {pedidos.length === 0 ? (
        <p>No tienes pedidos asignados.</p>
      ) : (
        <ul>
          {pedidos.map((pedido) => (
            <PedidoItem key={pedido.id} pedido={pedido} onUpdate={fetchPedidos}  />
          ))}
        </ul>
      )}
    </div>
  );
};

export default Dashboard;
