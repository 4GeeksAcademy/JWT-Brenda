import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const Private = () => {
    const navigate = useNavigate();

    useEffect(() => {
        const token = sessionStorage.getItem('token');
        if (!token) {
            navigate('/login');
        }
    }, [navigate]);

    return <h1>Bienvenido a la página privada</h1>;
};

export default Private;
