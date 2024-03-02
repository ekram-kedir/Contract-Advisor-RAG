import Link from "next/link";
import React from "react";
interface NoServicesProps {
  id: string;
}
const NoServices: React.FC<NoServicesProps> = ({ id }) => {
  return (
    <div className="text-gray-500 text-center">
      <span>There is no service data for this hospital at the moment.</span>
      <div>
        <Link href={`/hospitals/${id}`}>
          <div className="flex flex-wrap text-primary justify-center font-bold hover:text-blue-600">
            <span>{"Show more"}</span>
          </div>
        </Link>
      </div>
    </div>
  );
};

export default NoServices;
