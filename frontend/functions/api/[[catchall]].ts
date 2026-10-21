export const onRequest = async (context: any) => {
  const url = new URL(context.request.url);
  const targetUrl = new URL(url.pathname + url.search, 'https://grade-a-api.priyanshukh1201.workers.dev');
  return fetch(new Request(targetUrl.toString(), context.request));
};
