'use client'
import { useChat } from 'ai/react'

export function Chat() {
    const {messages, input, handleInputChange, handleSubmit} = useChat()

    return(
        <div className='flex flex-col max-w-xl px-8 max-auto'>
            {
                messages.map(message=>{
                    const isBot = message.role != 'user'
                    return(
                    <div key={message.id}>
                        <p>
                            {isBot ? '🤖' : '🧑‍💻'}
                            <span className={`${ isBot ? 'text-yellow-500' : 'text-blue-300'}`}>{message.content}</span>
                        </p>
                    </div>
                    )
                })
            }
            <form className= 'fixed bottom-4 w-full' onSubmit={handleSubmit}>
                <input className='max-w-xs m-auto py-2 px-4 rounded-full' placeholder='Consulta...' type='text' name='content' value={input} onChange={handleInputChange} />
            </form>
        </div>
    )
}