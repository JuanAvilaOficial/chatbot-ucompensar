'use client'
import { useChat } from 'ai/react'

export function Chat() {
    const {messages, input, handleInputChange, handleSubmit} = useChat()

    return(
        <div className='flex flex-col max-w-xl px-8 max-auto'>
            {
                messages.map(message => {
                    const isUser = (message.role == 'user')
                    return(
                        <div key={message.id}>
                            <p>
                                {isUser ? '🧑‍💻' : '🤖'}

                                <span className={`pl-2 ${ isUser ? 'text-yellow-500' : 'text-blue-300'}`}>{message.content}</span>
                            </p>
                        </div>
                    )
                })
            }
            <form  onSubmit={handleSubmit}>
                <input className='fixed w-full max-w-xl px-4 py-2 mb-8 border border-gray-400 rounded-full shadow-2xl bottom-4' placeholder='Consulta...' type='text' name='content' value={input} onChange={handleInputChange} />
            </form>
        </div>
    )
}