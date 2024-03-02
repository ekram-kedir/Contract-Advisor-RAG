import React from "react";
import { render, screen } from "@testing-library/react";
import LoadingPage from "@/components/commons/Loading";

describe("LoadingPage component", () => {
  test("renders the LoadingPage component correctly", () => {
    render(<LoadingPage />);

    const loadingElement = screen.getByTestId("loading-spinner");
    expect(loadingElement).toBeInTheDocument();
    expect(loadingElement).toHaveClass("animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-primary");
  });

  test('render the 2 divs correctly',() => {
    render(<LoadingPage />)

    const divElements = screen.getAllByRole('load');
    expect(divElements.length).toBe(2);
  })
});