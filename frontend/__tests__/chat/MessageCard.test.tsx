import React from "react";
import { render } from "@testing-library/react";
import { Provider } from "react-redux";
import {store} from "../../store/index"; 
import MessageCard from "../../components/chat/MessageCard";
describe("MessageCard component", () => {
  test("renders the outer div", () => {
    const { getByTestId } = render(
      <Provider store={store}>
        <MessageCard />
      </Provider>
    );
    const outerDiv = getByTestId("message-card");
    expect(outerDiv).toBeInTheDocument();
  });
});