export default interface ServiceType {
    id: number
    title: string
    detail: string
  }

export interface ChatResponse {
    isSuccess: boolean;
    value: {
      text: string;
      timestamp:number;
      sender:string;
    };
  }
  

export interface MessageHistory{
  content:string[];
  type:string;

}
export interface Institution {
    institutionName: string;
    branchName: string;
    website: string;
    phoneNumber: string;
    summary: string;
    establishedOn: string;
    rate: number;
    status: string;
    allEducationalInstitutions: null;
    allSpecialities: null;
    logoUrl: string;
    bannerUrl: string;
    address: Address;
    services: string[];
    photos: string[];
    id: string;
  }
  
 export  interface AttachemntResponse {
    success: boolean; // Example property, adjust according to your actual response
    message?: string; // Example property, adjust according to your actual response
    // Add more properties as needed based on your actual response
  }
  
  interface Address {
    country: string;
    region: string;
    zone: string;
    woreda: string;
    city: string;
    subCity: string;
    longitude: number;
    latitude: number;
    summary: string;
    id: string;
  }
  interface Education {
    EducationInstitution:string;
    StartYear:Date;
    Degree:string;
    FieldOfStudy:string;
    EducationInstitutionLogoUrl:string;
    GraduationYear:Date;
  }
 export interface Query {
   message: string;
   timestamp:number;
  }
 
  
  export interface MessageBody {
    message:string,
    Address:string,
    isNewChat:boolean
  }
  export interface IpState {
    ipAddress: string ;
  }



//   import { Query } from '@/types/chat/chat-types';
// import { PayloadAction, createSlice } from '@reduxjs/toolkit';
// export interface MessageHistory {
//     messages:(string |Query)[];
// }
// const initialState: MessageHistory = {
//     messages: [], 
// };
// const ChatHistory = createSlice({
//   name: 'ChatHistory',
//   initialState,
//   reducers: {
//     addMessage(state, action: PayloadAction<MessageHistory>) {
//       // Check the type of the payload and handle accordingly
//       if (typeof action.payload === 'string') {
//         state.messages.push({
//           message: action.payload,
//           timestamp: Date.now(), // Add current timestamp when adding a message
//         });
//       } 
//     },
//     clearMessages(state) {
//       state.messages = [];
//     },
//   },
// });
// export const {addMessage, clearMessages} = ChatHistory.actions
// export default ChatHistory