import React from 'react'

const LogCard = ({ logIndex, logMessage }) => {
    return (
        <div className='flex flex-row rounded-lg min-w-2xl border border-bg-gray-400 justify-between p-4'>
            <div className='flex flex-row w-96 gap-4'>
                <h3 className='w-12 text-sm font-bold'>Log {logIndex}</h3>
                <p>{logMessage}</p>
            </div>
            <div className='bg-red-100 p-2 rounded-lg align-center'>
                Status: CRITICAL
            </div>

        </div>
    )
}

export default LogCard