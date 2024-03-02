import { ChatBot } from "@/store/features/chat/chat-api";
import IpSlice from "@/store/features/chat/ip-slice";
import ChatHistory from "@/store/features/chat/message-history";
import { configureStore } from "@reduxjs/toolkit";

export const store = configureStore({
  reducer: {
    [ChatBot.reducerPath]: ChatBot.reducer,
    ChatHistory: ChatHistory.reducer,
    IpSlice: IpSlice.reducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware()
      .concat(ChatBot.middleware)
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
