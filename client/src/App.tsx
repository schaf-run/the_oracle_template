import { BrowserRouter, Routes, Route } from "react-router-dom";
import { UploadPage } from "./pages/UploadPage";
import { ViewerPage } from "./pages/ViewerPage";

export function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<UploadPage />} />
        <Route path="/model/:id" element={<ViewerPage />} />
      </Routes>
    </BrowserRouter>
  );
}
