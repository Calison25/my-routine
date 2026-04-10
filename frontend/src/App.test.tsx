import { render, screen } from "@testing-library/react";
import { describe, it, expect } from "vitest";
import App from "./App";

describe("App", () => {
  it("should render the application title", () => {
    render(<App />);

    expect(screen.getByText("My Routine")).toBeInTheDocument();
  });
});
