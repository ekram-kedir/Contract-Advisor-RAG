import React from "react";
import { ReactNode, Suspense } from "react";
import { useRouter } from "next/router";
import Loading from "@/components/commons/Loading";
const RootLayout = ({ children }: { children: ReactNode }) => {
  const router = useRouter();
  const isChatPage = router.pathname === "/chat";

  return (
    <div>
      <Suspense fallback={<Loading />}>{children}</Suspense>
    </div>
  );
};

export default RootLayout;
