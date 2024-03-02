import { ChatResponse } from '@/types/chat/chat-types';
import { PayloadAction, createSlice } from '@reduxjs/toolkit';
export interface MessageHistory {
    messages:(string|ChatResponse)[];
}
const initialState: MessageHistory = {
    messages: [], 
};
const ChatHistory = createSlice({
    name: 'ChatHistory',
    initialState,
    reducers: {
      addMessage(state, action: PayloadAction<string | ChatResponse>) {
        state.messages.push(action.payload);
      },
      clearMessages(state) {
        state.messages = [];
      },
    },
  });
export const {addMessage, clearMessages} = ChatHistory.actions
export default ChatHistory