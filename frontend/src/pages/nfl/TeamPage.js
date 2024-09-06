import React from 'react';
import { useParams } from 'react-router-dom';


const TeamPage = () => {
    const { teamName } = useParams();




    return(
        <div>{teamName} page coming soon!</div>
    );
};

export default TeamPage;