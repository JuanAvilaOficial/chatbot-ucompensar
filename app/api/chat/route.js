import {Configuration, OpenAIApi } from 'openai-edge'
import { OpenAIStream, streamText } from 'ai';
//import { createOpenAI } from '@ai-sdk/openai';

//import { streamText } from 'ai';
//import { openai } from '@ai-sdk/openai'

export const runtime = 'edge';

// Crear cliente de OpenAI
const config = createOpenAI({
    apiKey: env.OPENAI_API_KEY
});

const openai = new OpenAIApi(config);

export async function POST(request) {
    const response = await openai.createChatCompletion({
        model: "gpt-3.5-turbo",
        stream: true,
        messages: 
        [{
            role: 'system',
            content : 'Comportate como un chatbot para universidad que responde preguntar sobre los procesos',

        },
        {
            role: 'user',
            content: 'Hola, ¿qué es el proceso de compensación?',
        },],
        max_tokens: 1000,
        temperature: 0.7,
        top_p: 1,
        frequency_penalty: 1,
        presence_penalty: 1, 
    })
    //response.choices[0].message
    console.log(response)
    const stream = OpenAIStream(response)
    return new streamText(stream)
}