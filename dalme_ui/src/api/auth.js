import { apiUrl, dbUrl, fetchApi, headers } from "@/api/config";

const auth = {
  async logout() {
    const url = `${dbUrl}/logout/`;
    const request = new Request(url, { method: "POST", headers: headers });

    const response = await fetchApi(request);

    if (response.redirected) {
      window.location.href = response.url;
    }
  },

  async session() {
    const url = `${apiUrl}/session/retrieve/`;
    const request = new Request(url);

    const response = await fetchApi(request);
    const data = await response.json();

    return { success: response.ok, data };
  },
};

export default auth;
