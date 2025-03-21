import React from 'react';
import { iniciarPedido, finalizarPedido } from '../../services/api';

interface Pedido {  // Define la interfaz Pedido (¡Importante en TypeScript!)
    id: number;
    cliente: string;
    conductor: string | null;
    origen: string;
    destino: string;
    descripcion: string;
    estado: 'pendiente' | 'en_curso' | 'finalizado' | 'cancelado';
    fecha_creacion: string; //  Puedes usar Date si prefieres
    fecha_inicio: string | null;
    fecha_fin: string | null;
}
interface PedidoItemProps {
  pedido: Pedido; // Usamos la interfaz Pedido
  onUpdate: () => void;
}

const PedidoItem: React.FC<PedidoItemProps> = ({ pedido, onUpdate }) => {

  const handleIniciar = async () => {
    try {
      // Primero muestra la info
      const confirmacion = await iniciarPedido(pedido.id);
      console.log(confirmacion);

      // Aquí, en lugar de un alert, usarías un modal o un componente
      // de confirmación de tu librería de UI preferida.

        const confirmado = window.confirm('¿Deseas iniciar el pedido?');

        if(confirmado){
            await iniciarPedido(pedido.id);
            onUpdate(); // Actualiza la lista
        }


    } catch (error) {
      console.error("Error al iniciar el pedido:", error);
    }
  };

  const handleFinalizar = async () => {
    try {
        const confirmacion = await finalizarPedido(pedido.id);
        console.log(confirmacion);
        const confirmado = window.confirm("¿Desea finalizar el pedido?");
        if(confirmado){
            await finalizarPedido(pedido.id);
            onUpdate();
        }

    } catch (error) {
      console.error("Error al finalizar el pedido:", error);
    }
  };

  return (
    <li>
      <div>ID: {pedido.id}</div>
      <div>Origen: {pedido.origen}</div>
      <div>Destino: {pedido.destino}</div>
      <div>Estado: {pedido.estado}</div>
      {/* Muestra más detalles aquí */}
      {pedido.estado === 'pendiente' && (
        <button onClick={handleIniciar}>Iniciar Viaje</button>
      )}
      {pedido.estado === 'en_curso' && (
        <button onClick={handleFinalizar}>Finalizar Viaje</button>
      )}
    </li>
  );
};

export default PedidoItem;
