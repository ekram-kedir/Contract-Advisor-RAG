import { ChatResponse, MessageBody, MessageHistory , AttachemntResponse } from "@/types/chat/chat-types"
import {createApi, fetchBaseQuery} from "@reduxjs/toolkit/query/react"
const API_BASE_URL = 'http://127.0.0.1:5000'
export const ChatBot = createApi({
    reducerPath:'ChatBot',
    baseQuery:fetchBaseQuery({baseUrl:API_BASE_URL}),
    endpoints:(builder) => ({
        postChatBot: builder.mutation<ChatResponse, MessageBody>({
            query: (body) => ({
                url:'/api/v1/chat',
                method:"POST",
                body:body

            }),
          }),
        fetchMessages: builder.query<MessageHistory[], void>({
            query: () => '/api/v1/messages', // Replace with your actual endpoint for fetching messages
        }),
        uploadAttachment: builder.mutation<AttachemntResponse, FormData>({
            query: (formData) => ({
                url: '/api/v1/upload',
                method: "POST",
                body: formData,
                headers: {
                    'Content-Type': 'multipart/form-data', // Ensure proper content type for file upload
                }
            }),
    })
})

})
export const { usePostChatBotMutation, useFetchMessagesQuery, useUploadAttachmentMutation } = ChatBot;
