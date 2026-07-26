import type { Directive } from "vue";
import type { HighlightDirective, RippleDirective } from "@/directives";

declare module "vue" {
  export interface GlobalDirectives {
    vHasPerm: Directive;
    vRipple: RippleDirective;
    vHighlight: HighlightDirective;
  }
}
