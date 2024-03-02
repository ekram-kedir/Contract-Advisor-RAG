import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { IpState } from '@/types/chat/chat-types';
const initialState: IpState = {
  ipAddress:'',
};
const IpSlice = createSlice({
  name: 'ipaddress',
  initialState,
  reducers: {
    setIpAddress: (state, action: PayloadAction<string>) => {
      state.ipAddress = action.payload;
    },
  },
});
export const { setIpAddress } = IpSlice.actions;
export default IpSlice;
