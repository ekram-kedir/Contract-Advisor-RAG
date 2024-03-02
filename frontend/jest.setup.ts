import "@testing-library/jest-dom";
import "match-media-mock";
import { TextEncoder, TextDecoder } from "text-encoding";

window.matchMedia =
  window.matchMedia ||
  function () {
    return {
      matches: false,
      addListener: function () {},
      removeListener: function () {},
    };
  };

(global as any).TextEncoder = TextEncoder;
(global as any).TextDecoder = TextDecoder;