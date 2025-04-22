import React from 'react'

const LogCard = ({ logIndex, logMessage, logLevel }) => {
    return (
        <div className='flex flex-row rounded-lg min-w-2xl border border-bg-gray-400 justify-between p-4'>
            <div className='flex flex-row w-96 gap-4'>
                <h3 className='w-12 text-sm font-bold'>Log {logIndex}</h3>
                <p>{logMessage}</p>
            </div>

            {logLevel == 'CRITICAL' ? (<div className='bg-red-100 p-2 w-32 rounded-lg align-center'>
                CRITICAL
            </div>) : ''}

            {logLevel == 'INFO' ? (<div className='bg-green-300 p-2 w-32 rounded-lg align-center'>
                INFO
            </div>) : ''}

            {logLevel == 'WARNING' ? (<div className='bg-red-800 p-2 w-32 rounded-lg align-center'>
                WARNING
            </div>) : ''}

            {logLevel == 'ERROR' ? (<div className='bg-yellow-300 p-2 w-32 rounded-lg align-center'>
                ERROR
            </div>) : ''}

        </div>
    )
}

export default LogCard
